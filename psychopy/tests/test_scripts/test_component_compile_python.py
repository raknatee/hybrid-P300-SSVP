import os
import shutil
from tempfile import mkdtemp
from psychopy.experiment import getAllComponents, Experiment
from psychopy.tests.utils import compareTextFiles, TESTS_DATA_PATH
from psychopy.scripts import psyexpCompile


class TestComponentCompilerPython(object):
    """A class for testing the Python code compiler for all components"""
    def setup(self):
        self.temp_dir = mkdtemp()
        self.allComp = getAllComponents(fetchIcons=False)
        self.exp = Experiment() # create once, not every test
        self.exp.addRoutine('trial')
        self.exp.flow.addRoutine(self.exp.routines['trial'], pos=0)
        # Create correctScript subdir for holding correct scripts
        if not os.path.isdir(os.path.join(TESTS_DATA_PATH, "correctScript", "python")):
            os.mkdir(os.path.join(TESTS_DATA_PATH, "correctScript", "python"))

    def teardown(self):
        shutil.rmtree(self.temp_dir)

    def test_all_components(self):
        """Test all component code outputs, except for Settings and Unknown"""
        for compName in self.allComp:
            if compName not in ['SettingsComponent', 'UnknownComponent']:
                # reset exp
                self.reset_experiment()
                # Add components
                self.add_components(compName)
                # Create output script
                self.create_component_output(compName)
                # Get correct script path
                # correctPath = os.path.join(TESTS_DATA_PATH, "correctScript", "python", 'correct{}.py'.format(compName))
                # Compare files, raising assertions on fails above tolerance (%)
                # try:
                #     compareTextFiles('new{}.py'.format(compName), correctPath, tolerance=5)
                # except IOError as err:
                #     compareTextFiles('new{}.py'.format(compName), correctPath, tolerance=5)

    def reset_experiment(self):
        """Resets the exp object for each component"""
        self.exp = Experiment()
        self.exp.addRoutine('trial')
        self.exp.flow.addRoutine(self.exp.routines['trial'], pos=0)

    def add_components(self, compName):
        """Add components to routine"""
        thisComp = self.allComp[compName](parentName='trial', exp=self.exp)
        if compName == 'StaticComponent':
            # Create another component to trigger param updates for static
            textStim = self.allComp['TextComponent'](parentName='trial', exp=self.exp)
            textStim.params['color'].allowedUpdates.append('set during: trial.ISI')
            textStim.params['color'].updates = 'set during: trial.ISI'
            self.exp.routines['trial'].addComponent(textStim)
            # Create static component
            thisComp.addComponentUpdate('trial', 'text', 'color')
            thisComp.params['code'].val = "customStaticCode = True"  # Add the custom code
            self.exp.routines['trial'].addComponent(thisComp)
        else:
            self.exp.routines['trial'].addComponent(thisComp)

    def create_component_output(self, compName):
        """Create the Python script"""
        pyFilePath = os.path.join(self.temp_dir, 'new{}.py'.format(compName))
        psyexpCompile.compileScript(infile=self.exp, outfile=pyFilePath)

    def test_component_type_in_experiment(self):
        for compName in self.allComp:
            if compName not in ['SettingsComponent', 'UnknownComponent']:
                # reset exp
                self.reset_experiment()
                # Add components
                self.add_components(compName)
                # Check component in exp
                component = compName.split('Component')[0]
                assert self.exp.getComponentFromType(component)
