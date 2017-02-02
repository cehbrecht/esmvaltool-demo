from malleefowl import config

from esmvalwps.process import ESMValToolProcess
from esmvalwps import runner

from malleefowl import wpslogging as logging
logger = logging.getLogger(__name__)

class PerfmetricsTaylorProcess(ESMValToolProcess):
    def __init__(self):
        ESMValToolProcess.__init__(self,
            identifier = "taylor",
            title = "ESMValTool: Perfmetrics  Taylor",
            version = "0.1",
            abstract="Plotting the Taylor diagram of the performance metrics for the CMIP5 models."
            )

        self.variable = self.addLiteralInput(
            identifier="variable",
            title="Variable",
            abstract="",
            type=type(''),
            minOccurs=1,
            maxOccurs=1,
            allowedValues=['ta', 'ua', 'va', 'zg', 'tas', 'rsut', 'rlut']
            )

    def execute(self):
        self.show_status("starting", 0)

        constraints= runner.build_constraints(
            project="CMIP5",
            models=self.getInputValues(identifier='model'),
            variable=self.variable.getValue(),
            cmor_table=self.cmor_table.getValue(),
            experiment=self.experiment.getValue(),
            ensemble=self.ensemble.getValue())

        out, namelist, log_file, reference = runner.diag(
            name="taylor",
            credentials=self.credentials.getValue(),
            constraints=constraints,
            start_year=self.start_year.getValue(),
            end_year=self.end_year.getValue(),
            output_format=self.output_format.getValue(),
            monitor=self.show_status)

        self.show_status("done", 100)

        self.output.setValue(out)
        self.namelist.setValue(namelist)
        self.log.setValue(log_file)
        self.reference.setValue(reference)
