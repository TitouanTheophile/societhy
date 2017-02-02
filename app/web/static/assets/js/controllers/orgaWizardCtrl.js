'use strict';
/** 
  * controller for Wizard Form example
  */


  app.controller('OrgaWizardCtrl', 
    function ($scope, $http, ngNotify, FileUploader, $sessionStorage, $rootScope) {
        $scope.currentStep = 1;


    // IMAGE UPLOAD
    var uploaderImages = $scope.uploaderImages = new FileUploader({
        headers: {
            Authentification: $sessionStorage.SociethyToken
        },
    });

    uploaderImages.filters.push({
        name: 'imageFilter',
        fn: function (item, options) {
            var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
            return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
        }
    });

    uploaderImages.onBeforeUploadItem = function (item) {
        console.info('onBeforeUploadItem', item);
    };
    uploaderImages.onErrorItem = function (fileItem, response, status, headers) {
        console.info('onErrorItem', fileItem, response, status, headers);
    };
    uploaderImages.onCompleteItem = function (fileItem, response, status, headers) {
        console.info('onCompleteItem', fileItem, response, status, headers);
    };

    // PAGE MANAGEMENT
    $scope.form = {

        next: function (form) {

            $scope.toTheTop();

            if (form.$valid) {
                form.$setPristine();
                nextStep();
            } else {
                console.log(form);
                var field = null, firstError = null;
                for (field in form) {
                    if (field[0] != '$') {
                        if (firstError === null && !form[field].$valid) {
                            firstError = form[field].$name;
                        }

                        if (form[field].$pristine) {
                            form[field].$dirty = true;
                        }
                    }
                }
                console.log(firstError)
                angular.element('.ng-invalid[name=' + firstError + ']').focus();
                errorMessage('please complete the form in this step before proceeding');
            }
        },

        prev: function (form) {
            $scope.toTheTop();
            prevStep();
        },

        goTo: function (form, i) {
            if (parseInt($scope.currentStep) > parseInt(i)) {
                $scope.toTheTop();
                goToStep(i);

            } else {
                if (form.$valid) {
                    $scope.toTheTop();
                    goToStep(i);

                } else
                errorMessage('please complete the form in this step before proceeding');
            }
        },

        submit: function (form) {
            if (!$rootScope.user.account) {
                errorMessage("Please set up an ethereum account first")
            }
            else {
                $scope.completeBlockchainAction(function(password, newOrga) {
                    $rootScope.toogleWait("Processing organization creation...");
                    $http.post('/createOrga', {
                        "password": password,
                        "newOrga" : {
                            "name": form.name.$$rawModelValue,
                            "description" : form.description.$$rawModelValue,
                            "type" : form.type.$$rawModelValue,
                            "fbUrl": form.fbUrl.$$rawModelValue,
                            "twitterUrl" : form.twitterUrl.$$rawModelValue
                        }}).then(function(response) {
                            console.log("resp =", response, $rootScope.user);
                        }, function(error) {
                            $rootScope.toogleError(error.data);
                         });
                }, form);
            }
        },

        reset: function () {

        }
    };


    var nextStep = function () {
        $scope.currentStep++;
    };
    var prevStep = function () {
        $scope.currentStep--;
    };
    var goToStep = function (i) {
        $scope.currentStep = i;
    };

    var errorMessage = function (text) {

        ngNotify.set(text, {
            theme: 'pure',
            position: 'top',
            type: 'error',
            button: 'true',
            sticky: false,
            duration: 3000
        });
    };
});
