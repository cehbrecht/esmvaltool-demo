from pywps import Process
from pywps import LiteralInput, LiteralOutput
from pywps import ComplexInput, ComplexOutput
from pywps import Format, FORMATS
from pywps.app.Common import Metadata

from esmvalwps import runner

import logging
LOGGER = logging.getLogger("PYWPS")


class MyDiag(Process):
    def __init__(self):
        inputs = [
            LiteralInput('model', 'Model',
                         abstract='Choose a model like MPI-ESM-LR.',
                         data_type='string',
                         allowed_values=['MPI-ESM-LR', 'MPI-ESM-MR'],
                         default='MPI-ESM-LR'),
            LiteralInput('experiment', 'Experiment',
                         abstract='Choose an experiment like historical.',
                         data_type='string',
                         allowed_values=['historical', 'rcp26', 'rcp45', 'rcp85'],
                         default='historical'),
            # LiteralInput('time_frequency', 'Time frequency',
            #              abstract='Choose a time frequency like mon.',
            #              data_type='string',
            #              allowed_values=['mon', 'day'],
            #              default='mon'),
            LiteralInput('ensemble', 'Ensemble',
                         abstract='Choose an ensemble like r1i1p1.',
                         data_type='string',
                         allowed_values=['r1i1p1', 'r2i1p1', 'r3i1p1'],
                         default='r1i1p1'),
            LiteralInput('start_year', 'Start year', data_type='integer',
                         abstract='Start year of model data.',
                         default="1990"),
            LiteralInput('end_year', 'End year', data_type='integer',
                         abstract='End year of model data.',
                         default="2000"),
        ]
        outputs = [
            ComplexOutput('namelist', 'namelist',
                          abstract='ESMValTool namelist used for processing.',
                          as_reference=True,
                          supported_formats=[Format('text/plain')]),
            ComplexOutput('log', 'Log File',
                          abstract='Log File of ESMValTool processing.',
                          as_reference=True,
                          supported_formats=[Format('text/plain')]),
            ComplexOutput('output', 'Output plot',
                          abstract='Generated output plot of ESMValTool processing.',
                          as_reference=True,
                          supported_formats=[Format('application/pdf')]),
        ]

        super(MyDiag, self).__init__(
            self._handler,
            identifier="mydiag",
            title="ESMValTool: tutorial diagnostic.",
            version="1.0",
            abstract="Tutorial diagnostic used in the doc/toy-diagnostic-tutorial.pdf.",
            # profile=['birdhouse'],
            metadata=[
                Metadata('Birdhouse', 'http://bird-house.github.io/'),
                Metadata('ESMValTool', 'http://www.esmvaltool.org/')],
            inputs=inputs,
            outputs=outputs,
            status_supported=True,
            store_supported=True)

    def _handler(self, request, response):
        # build esgf search constraints
        constraints = dict(
            model=request.inputs['model'][0].data,
            experiment=request.inputs['experiment'][0].data,
            time_frequency='mon',  # request.inputs['time_frequency'][0].data,
            ensemble=request.inputs['ensemble'][0].data,
        )
        if constraints['time_frequency'] == 'mon':
            constraints['cmor_table'] = 'Amon'
        else:
            constraints['cmor_table'] = 'day'

        # generate namelist
        result = runner.diag(
            'mydiag',
            constraints=constraints,
            start_year=request.inputs['start_year'][0].data,
            end_year=request.inputs['end_year'][0].data,
            output_format='pdf')

        # namelist output
        response.outputs['namelist'].output_format = FORMATS.TEXT
        response.outputs['namelist'].file = result['namelist']

        # log output
        response.outputs['log'].output_format = FORMATS.TEXT
        response.outputs['log'].file = result['logfile']

        # find result plot
        # response.outputs['output'].output_format = FORMATS.PDF
        response.outputs['output'].file = result['output']


        return response
