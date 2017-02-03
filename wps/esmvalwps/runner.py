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


def diag(name, constraints, start_year, end_year, output_format='pdf', workspace=None):
    # TODO: maybe use result dict
    result = {}
    workspace = workspace or os.curdir

    try:
        result['namelist'] = generate_namelist(
            diag=name,
            workspace=workspace,
            constraints=constraints,
            start_year=start_year,
            end_year=end_year,
            output_format=output_format,
        )

        # run diag
        result['logfile'] = run_diag(result['namelist'], workspace)

        # references/acknowledgements document
        result['reference'] = os.path.join(workspace, 'work', 'namelist.txt')

        # plot output
        result['output'] = find_plot(workspace, output_format)
    except:
        LOGGER.exception("diag %s failed!", name)
        raise
    return result


def run_diag(namelist, workspace='.'):
    # ncl path
    LOGGER.debug("NCARG_ROOT=%s", os.environ.get('NCARG_ROOT'))

    # build cmd
    script = os.path.join(ESMVAL_ROOT, "esmval.sh")
    logfile = os.path.abspath(os.path.join(workspace, 'log.txt'))
    cmd = [script, namelist, logfile]

    # run cmd
    try:
        check_output(cmd, stderr=STDOUT)
    except:
        LOGGER.exception('esmvaltool failed!')

    # debug: show logfile
    if LOGGER.isEnabledFor(logging.DEBUG):
        with open(logfile, 'r') as f:
            LOGGER.debug(f.read())

    # check if data is found
    if os.path.isfile(os.path.join(workspace, 'esgf_coupling_report.txt')):
        raise Exception("Could not find data in ESGF archive.")

    return logfile


def generate_namelist(diag, constraints=None, start_year=2000, end_year=2005, output_format='pdf', workspace='.'):
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
