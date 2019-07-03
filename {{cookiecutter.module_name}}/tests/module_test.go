package testing

import (
  //"os"
  "testing"

  //"github.com/gruntwork-io/terratest/modules/random"
  "github.com/gruntwork-io/terratest/modules/terraform"
)

func TestModule(t *testing.T) {
  //resourceName := random.UniqueId()

  terraformOptions := &terraform.Options{
    // The path to where your Terraform code is located
    TerraformDir: "../",

    // Disable color output
    NoColor: true,

    // Variables to pass to our Terraform code using -var options
    //Vars: map[string]interface{}{
    //	"resource_name":          resourceName,
    //	"aws_region":             os.Getenv("AWS_REGION"),
    //}
  }

  // At the end of the test, run `terraform destroy` to clean up any resources that were created
  defer terraform.Destroy(t, terraformOptions)

  // This will run `terraform init` and `terraform apply` and fail the test if there are any errors
  terraform.InitAndApply(t, terraformOptions)
}
