angular.module('resto.controllers', [])
.controller('RootController', ($scope,$location, $http)->
  
  $scope.auth = auth;
  $scope.loginform = {
    'username':''
    'password':''
  }
  $scope.login = ->
    $http.post('api/login', $scope.loginform)
      .success((data) ->
        if data.success
          $scope.auth = true
          $scope.loggingin = false
      )
      .error((data) ->
        console.log(data)
      )

  $scope.logout = ->
    $http.get('/api/logout')
      .success((data) ->
        $scope.auth = false
        $scope.loginform['username'] = ''
        $scope.loginform['password'] = ''
        $location.url('/#/home')
     )
)

.controller('RegisterController', ($scope, $location, $http) ->

  $scope.userform = {
    'email':'',
    'firstname': '',
    'lastname': '',
    'birthday': '',
    'adress': '',
    'tel': '',
    'password': ''
  }

  $scope.submit = ->
    $http.post('/api/register', $scope.userform)
      .success((data) ->
        console.log(data)
      )
      .error((data) ->
        console.log(data)
      )
)

.controller('UserController', ($scope, $location, $http) ->
  
  $http.get('/api/profile')
    .success((data) ->
      $scope.profiles = data.users
    ).error((data) ->
      console.log(data)
    )

  $scope.edit = (profile) ->
    profile.backup = _.clone(profile)
    profile.backup.user = _clone(profile.user)

  $scope.cancel = (profile) ->
    profile = profile['backup']

  $scope.save = (profile) ->
    $http.post('/api/edit_profile', profile)
      .success((data) ->
        console.log(data)
        delete profile['backup']
      )      
)
