angular.module('resto.userControllers', [])
.controller 'RootController', ($scope, $location, $http) ->
  $scope.auth = auth
  $scope.username = username
  
  $scope.loginform = {
    'username':''
    'password':''
  }
  $scope.login = ->
    $http.post('api/login', $scope.loginform)
      .success (data) ->
        if data.success
          $scope.auth = true
          $scope.loggingin = false
          $scope.username = data.username
      .error (data) ->
        console.log(data)

  $scope.logout = ->
    $http.get('/api/logout')
      .success (data) ->
        $scope.auth = false
        $scope.loginform['username'] = ''
        $scope.loginform['password'] = ''


.controller 'RegisterController', ($scope, $location, $http) ->

  $scope.userform = {
    'email':'',
    'first_name': '',
    'last_name': '',
    'date_naissance': '',
    'adresse': '',
    'telephone': '',
    'password': ''
  }

  $scope.submit = ()->
    $http.post('/api/register', $scope.userform)
      .success(data) ->
        alert('registration successful')
        console.log(data)
      .error (data) ->
        console.log(data)

.controller 'UserController', ($scope, $location, $http) ->

  if $location.path() == '/manage/users'
    $http.get('/api/all_profiles')
      .success (data) ->
        $scope.profiles = data
      .error (data) ->
        console.log(data)
  else
    $http.get('/api/profile')
      .success (data) ->
        $scope.profile = data
 
  $scope.edit = (profile) ->
    profile.backup = _.clone(profile)
    profile.backup.user = _.clone(profile.user)

  $scope.cancel = (profile) ->
    _.extend(profile, profile.backup);
    delete profile['backup']

  $scope.save = (profile) ->
    $http.post('/api/edit_profile', profile)
      .success (data) ->
        console.log(data)
        delete profile['backup']
