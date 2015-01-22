(function() {
  angular.module('resto.controllers', []).controller('RootController', function($scope, $location, $http) {
    $scope.auth = auth;
    $scope.username = username;
    $scope.loginform = {
      'username': '',
      'password': ''
    };
    $scope.login = function() {
      return $http.post('api/login', $scope.loginform).success(function(data) {
        if (data.success) {
          $scope.auth = true;
          $scope.loggingin = false;
          return $scope.username = data.username;
        }
      }).error(function(data) {
        return console.log(data);
      });
    };
    return $scope.logout = function() {
      return $http.get('/api/logout').success(function(data) {
        $scope.auth = false;
        $scope.loginform['username'] = '';
        return $scope.loginform['password'] = '';
      });
    };
  }).controller('RegisterController', function($scope, $location, $http) {
    $scope.userform = {
      'email': '',
      'first_name': '',
      'last_name': '',
      'date_naissance': '',
      'adresse': '',
      'telephone': '',
      'password': ''
    };
    return $scope.submit = function() {
      return $http.post('/api/register', $scope.userform).success(function(data) {
        return console.log(data);
      }).error(function(data) {
        return console.log(data);
      });
    };
  }).controller('UserController', function($scope, $location, $http) {
    if ($location.path() === '/manage/users') {
      $http.get('/api/all_profiles').success(function(data) {
        return $scope.profiles = data.users;
      }).error(function(data) {
        return console.log(data);
      });
    } else {
      $http.get('/api/profile').success(function(data) {
        return $scope.profile = data;
      });
    }
    $scope.edit = function(profile) {
      profile.backup = _.clone(profile);
      return profile.backup.user = _.clone(profile.user);
    };
    $scope.cancel = function(profile) {
      _.extend(profile, profile.backup);
      return delete profile['backup'];
    };
    return $scope.save = function(profile) {
      return $http.post('/api/edit_profile', profile).success(function(data) {
        console.log(data);
        return delete profile['backup'];
      });
    };
  });

}).call(this);
