pipeline {
  environment {
    registry = "ossuchas/happyrefundapi"
    registryCredential = 'docker_ossuchas'
    dockerImage = ''
    image_tag_number = 'v1.24.4'
  }
  agent any
  stages {
    stage('Cloning Git') {
      steps {
        git 'https://github.com/ossuchas/APAPIHappyRefund.git'
      }
    }
    stage('Building image') {
      steps{
        script {
          dockerImage = docker.build registry + ":" + image_tag_number
        }
      }
    }
    stage('Deploy Image') {
      steps{
        script {
          docker.withRegistry( '', registryCredential ) {
            dockerImage.push()
          }
        }
      }
    }
    /*stage('Remove Unused docker image') {
      steps{
        sh "docker rmi $registry:$BUILD_NUMBER"
      }
    }*/
  }
}
