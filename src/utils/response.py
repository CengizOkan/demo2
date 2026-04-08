from sdks.novavision.src.helper.package import PackageHelper
from components.DemoPackage1.src.models.PackageModel import PackageModel, DemoPackageConfigs, ConfigMainExecutor

def build_response(context):
    # PackageModel içindeki gerçek sınıf isimlerini kullanıyoruz
    packageConfigs = DemoPackageConfigs(executor=context.executor_config)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel