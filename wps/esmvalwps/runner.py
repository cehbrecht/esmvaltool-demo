import os
import os.path
import glob
from subprocess import check_output, STDOUT

from esmvalwps import config

import logging
LOGGER = logging.getLogger("PYWPS")

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
        LOGGER.exception("diag %s failed!", name)
        raise
    return out, namelist, log_file, reference


def run_esmvaltool(namelist, workspace='.'):
    # ncl path
    LOGGER.debug("NCARG_ROOT=%s", os.environ.get('NCARG_ROOT'))

    # build cmd
    script = os.path.join(ESMVAL_ROOT, "esmval.sh")
    log_file = os.path.abspath(os.path.join(workspace, 'log.txt'))
    cmd = [script, namelist, log_file]

    # run cmd
    try:
        check_output(cmd, stderr=STDOUT)
    except:
        LOGGER.exception('esmvaltool failed!')

    # debug: show logfile
    if LOGGER.isEnabledFor(logging.DEBUG):
        with open(log_file, 'r') as f:
            LOGGER.debug(f.read())
    return log_file


def generate_namelist(diag, constraints=None, start_year=2000, end_year=2005, workspace='.', output_format='pdf'):
    constraints = constraints or {}
    workspace = os.path.abspath(workspace)

    # write esgf_config.xml
    esgf_config_templ = mylookup.get_template('esgf_config.xml')
    rendered_esgf_config = esgf_config_templ.render_unicode(
        workspace=workspace,
        archive_root=config.archive_root(),
    )
    esgf_config_filename = os.path.abspath(os.path.join(workspace, "esgf_config.xml"))
    with open(esgf_config_filename, 'w') as fp:
        fp.write(rendered_esgf_config)

    # write namelist.xml
    namelist = 'namelist_{0}.xml'.format(diag)
    namelist_templ = mylookup.get_template(namelist)
    rendered_namelist = namelist_templ.render_unicode(
        diag=diag,
        prefix=ESMVAL_ROOT,
        workspace=workspace,
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
    LOGGER.debug("plot file found=%s", matches[0])
    return matches[0]
