from setuptools.command.develop import develop
from distutils.command.install import install
from subprocess import check_call


class DevelopCmd(develop):
    def run(self):
        """overwrite run command to install pre-commit hooks in dev mode"""
        check_call(["pre-commit", "install", "-t", "pre-commit", "-t", "commit-msg"])
        super().run()
        
        return
        
class InstallCmd(install):
    def run(self):
        """overwrite run command to install fontawsome package"""
        
        # subprocess.check_call(['npm', 'install'])
        # subprocess.check_call(['./node_modules/.bin/webpack', '-p'])
        super().run()
        
        return 
