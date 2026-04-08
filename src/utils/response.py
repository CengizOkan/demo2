from sdks.novavision.src.helper.package import PackageHelper
# PackageModel.py içindeki gerçek sınıf isimlerini buraya ekledik:
from components.DemoPackage.src.models.PackageModel import PackageModel, DemoPackageConfigs

def build_response(context):
    # context.executor_config kısmını Package.py içinde tanımlayacağız
    packageConfigs = DemoPackageConfigs(executor=context.executor_config)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel