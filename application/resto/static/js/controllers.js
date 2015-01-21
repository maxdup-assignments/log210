(function() {
  app.controller('RootController', function($scope, $location, $http) {
    $scope.auth = auth;
    $scope.loginform = {
      'username': '',
      'password': ''
    };
    $scope.login = function() {
      return $http.post('api/login', $scope.loginform).success(function(data) {
        if (data.success) {
          $scope.auth = true;
          return $scope.loggingin = false;
        }
      }).error(function(data) {
        return console.log(data);
      });
    };
    return $scope.logout = function() {
      return $http.get('/api/logout').success(function(data) {
        $scope.auth = false;
        $scope.loginform['username'] = '';
        $scope.loginform['password'] = '';
        return $location.url('/#/home');
      });
    };
  });

  app.controller('RegisterController', function($scope, $location, $http) {
    $scope.userform = {
      'email': 'asd',
      'firstname': 'asd',
      'lastname': 'asd',
      'birthday': '',
      'adress': '',
      'tel': '',
      'password': ''
    };
    return $scope.submit = function() {
      return $http.post('/api/register', $scope.userform).success(function(data) {
        return console.log(data);
      }).error(function(data) {
        return console.log(data);
      });
    };
  });

  app.controller('UserController', function($scope, $location, $http) {
    $http.get('/api/profile').success(function(data) {
      return $scope.profiles = data.users;
    }).error(function(data) {
      return console.log(data);
    });
    $scope.edit = function(profile) {
      profile.backup = _.clone(profile);
      return profile.backup.user = _clone(profile.user);
    };
    $scope.cancel = function(profile) {
      return profile = profile['backup'];
    };
    return $scope.save = function(profile) {
      return $http.post('/api/edit_profile', profile).success(function(data) {
        console.log(data);
        return delete profile['backup'];
      });
    };
  });

}).call(this);
