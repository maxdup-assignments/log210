(function() {
  angular.module('resto.restoControllers', []).controller('RestaurantController', function($scope, $location, $http) {
    $scope.restos = [];
    $http.get('/api/all_resto').success(function(data) {
      $scope.restos = data;
      return console.log(data);
    }).error(function(data) {
      return console.log(data);
    });
    $scope.new_resto = {
      'name': '',
      'menu': {},
      'user': ''
    };
    $scope.options = [];
    $scope.selected_staff = '';
    $http.get('/api/all_staff').success(function(data) {
      var user, _i, _len;
      for (_i = 0, _len = data.length; _i < _len; _i++) {
        user = data[_i];
        $scope.options.push({
          'label': user.email,
          'value': user.pk
        });
      }
      $scope.selected_staff = $scope.options[0];
      return $scope.new_resto.user = $scope.selected_staff.value;
    });
    $scope.create_resto = function() {
      return $http.post('/api/create_resto', $scope.new_resto).success(function(data) {
        $scope.restos.push(data);
        return $scope.new_resto = {
          'name': '',
          'menu': {},
          'user': $scope.selected_staff.value
        };
      }).error(function(data) {
        return console.log(data);
      });
    };
    $scope.edit_resto = function(resto) {
      resto.backup = _.clone(resto);
      resto.backup.user = _.clone(resto.user);
      return resto.new_user = $scope.options[0];
    };
    $scope.save_resto = function(resto) {
      console.log(resto.new_user.value, resto.user.pk);
      if (resto.new_user.value === resto.user.pk) {
        delete resto['new_user'];
      }
      delete resto['backup'];
      return $http.post('/api/edit_resto', resto).success(function(data) {
        return console.log(data);
      });
    };
    $scope.cancel_resto = function(resto) {
      _.extend(resto, resto.backup);
      delete resto['backup'];
      return delete resto['new_user'];
    };
    return $scope.delete_resto = function(resto) {
      return $http.post('/api/delete_resto', resto).success(function(data) {
        $scope.restos = _.without($scope.restos, resto);
        return console.log(data);
      }).error(function(data) {
        return console.log(data);
      });
    };
  });

}).call(this);
