import os
import os.path
import glob
from subprocess import check_output, STDOUT

import logging
logger = logging.getLogger("PYWPS")

from mako.lookup import TemplateLookup
mylookup = TemplateLookup(directories=[os.path.join(os.path.dirname(__file__), 'templates')],
                          output_encoding='utf-8', encoding_errors='replace')

ESMVAL_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')


def diag(name, constraints, start_year, end_year, output_format='ps'):
    # TODO: maybe use result dict
    out = namelist = log_file = reference = None

    try:
        namelist = generate_namelist(
            diag=name,
            workspace=workspace,
            constraints=constraints,
            start_year=start_year,
            end_year=end_year,
            output_format=output_format,
        )

        # run diag
        log_file = esmvaltool(namelist, workspace)

        # references/acknowledgements document
        reference = os.path.join(workspace, 'work', 'namelist.txt')

        # plot output
        out = find_plot(workspace, output_format)
    except:
        logger.exception("diag %s failed!", name)
        raise
    return out, namelist, log_file, reference


def run_esmvaltool(namelist, workspace='.'):
    # set ncl path
    # ncarg_root = '/home/pingu/opt/ncl'  # config.getConfigValue("esmvalwps", "ncarg_root")
    # os.environ['NCARG_ROOT'] = ncarg_root.strip()
    # os.environ['PATH'] = os.environ['NCARG_ROOT'] + '/bin' + ':' + os.environ['PATH']

    # build cmd
    script = os.path.join(ESMVAL_ROOT, "esmval.sh")
    log_file = os.path.abspath(os.path.join(workspace, 'log.txt'))
    cmd = [script, namelist, log_file]

    # run cmd
    try:
        check_output(cmd, stderr=STDOUT)
    except:
        logger.exception('esmvaltool failed!')

    # debug: show logfile
    if logger.isEnabledFor(logging.DEBUG):
        with open(log_file, 'r') as f:
            logger.debug(f.read())

    return log_file


def generate_namelist(diag, constraints=None, start_year=2000, end_year=2005, workspace='.', output_format='pdf'):
    if not constraints:
        constraints = {}

    namelist = 'namelist_{0}.xml'.format(diag)
    mytemplate = mylookup.get_template(namelist)
    rendered_namelist = mytemplate.render_unicode(
        diag=diag,
        prefix=ESMVAL_ROOT,
        workspace=os.path.abspath(workspace),
        constraints=constraints,
        start_year=start_year,
        end_year=end_year,
        output_format=output_format
    )
    outfile = os.path.abspath(os.path.join(workspace, "namelist.xml"))
    with open(outfile, 'w') as fp:
        fp.write(rendered_namelist)
    return outfile


def find_plot(workspace='.', output_format="pdf"):
    matches = glob.glob(os.path.join(workspace, 'work', 'plots', '*', '*.{0}'.format(output_format)))
    if len(matches) == 0:
        raise Exception("no result plot found in workspace/plots")
    elif len(matches) > 1:
        raise Exception("more then one plot found %s", matches)
    logger.debug("plot file found=%s", matches[0])
    return matches[0]
