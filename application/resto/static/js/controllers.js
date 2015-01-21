'use strict';

app.controller('RootController', function($scope, $location, $http) {

  $scope.auth = auth;
  console.log($scope.auth)
  $scope.loginform = {
    'username':'',
    'password':''
  };

  $scope.login = function(){
    console.log('login');
    $http.post('/api/login', $scope.loginform)
      .success(function(data){
        if (data.success){
          $scope.auth = true;
          $scope.loggingin = false;
        }
      })
      .error(function(data){
        console.log(data);
      });
  };

  $scope.logout = function(){
    $http.get('/api/logout')
      .success(function(data){
        $scope.auth = false;
      })
  }
});

app.controller('LoginController', function($scope, $location, $http){
  $scope.loginform = {
    'username':'',
    'password':''
  };
  
  $scope.btn_login = function(){
    $http.post('/api/login', $scope.loginform)
      .success(function(data){
        console.log(data);
      })
      .error(function(data){
        console.log(data);
      });
  };
});

app.controller('RegisterController', function($scope, $location, $http){

  $scope.userform = {
    'email':'',
    'firstname': '',
    'lastname': '',
    'birthday': '',
    'adress': '',
    'tel': '',
    'password': ''
  };

  $scope.submit = function(){
    $http.post('/api/register', $scope.userform)
      .success(function(data){
        console.log(data);
      })
      .error(function(data){
        console.log(data)
      });
  };
});

app.controller('UserController', function($scope, $location, $http){
  //the backup doesn't actually work right
  $scope.backup = {};

  $scope.edit = function(profile){
    $scope.backup = _.clone(profile);
    $scope.backup.user = _.clone(profile.user);
    profile.editing = true;
  };
  $scope.cancel = function(profile){
    _.extend(profile, $scope.backup);
    profile.editing = false;
  };
  $scope.save = function(profile){
    $http.post('/api/edit_profile', profile)
      .success(function(data){
        console.log(data);
        profile.editing = false;
      });
  };


  $http.get('/api/profile')
    .success(function(data){
      console.log(data);
      $scope.profiles = data.users;

    }).error(function(data){
      console.log(data);
    });
});
