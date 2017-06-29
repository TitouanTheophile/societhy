app.controller('ProjectMainController', function($rootScope, $scope, $http, $sessionStorage, $state) {
  var ctrl = this;

  onLoad = function() {
    $http.post('/getProject', {'id': $state.params._id}).then(function(response) {
      $scope.project = response.data;
      $scope.isMember = $rootScope.user._id in $scope.project.members;
      // desc = $scope.project.description.replace(/(\r\n|\n|\r)/g,"<br />");
      // $scope.project.description = desc;
    }, function(error) {
      $state.go('app.discoverprojects');
      $rootScope.toogleError("Project does not exist");
    });
  };

  ctrl.joinProject = function(tag) {
    if ($scope.doVerifications()) {
      $scope.completeBlockchainAction(
        function(password) {
          $rootScope.toogleWait("Joining...");
          $http.post('/joinProject', {
            "socketid": $rootScope.sessionId,
            "tag": "member",
            "proj_id": $scope.project._id,
            "password": password
          }).then(function(data) {}, function(error) {
            $rootScope.toogleError(error);
          });
        },
        function(data) {
          $scope.project.members = data.data.project.members;
          // $rootScope.user.projects.push(data.data.project);
          $scope.isMember = true;
        });
    }
  }

  ctrl.leaveProject = function() {

    if ($scope.doVerifications()) {
      $scope.completeBlockchainAction(
        function(password) {
          $rootScope.toogleWait("Leaving...");
          $http.post('/leaveProject', {
            "socketid": $rootScope.sessionId,
            "proj_id": $scope.project._id,
            "password": password
          }).then(function(data) {}, function(error) {
            $rootScope.toogleError(error);
          });
        },
        function(data) {
          $scope.project.members = data.data.project.members;
          $scope.isMember = false;
        });
    }
  }

  ctrl.donateToProject = function() {
    // OUVRIR UNE JOLIE SWAL POUR DEMANDER LE MONTANT!
    donationAmount = $("#donationAmount").val();
    if (donationAmount > 0 && $scope.doVerifications()) {
      $scope.completeBlockchainAction(
        function(password) {
          $rootScope.toogleWait("Sending donation")
          $http.post('/donateToProject', {
            "socketid": $rootScope.sessionId,
            "proj_id": $scope.project._id,
            "donation": {
              "amount": donationAmount
            },
            "password": password
          }).then(function(data) {}, function(error) {
            $rootScope.toogleError(error);
          });
        },
        function(data) {
          $scope.project.balance = data.data;
          ctrl.wallet.refreshAllBalances();
        })
    } else {
      $rootScope.toogleError("Donation amount must be more than to 0...")
    }
  }

  onLoad();
  return ctrl;
});
