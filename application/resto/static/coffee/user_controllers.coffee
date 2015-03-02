angular.module('resto.userControllers', [])
.controller 'RootController', ($scope, $location, $http, $route) ->
  $scope.auth = auth == 'True'

  $http.get('/api/profile')
    .success (data) ->
      $scope.profile = data

  $scope.loginform = {
    'username':''
    'password':''
  }

  $scope.login = ->
    $http.post('api/login', $scope.loginform)
      .success (data) ->
        $scope.auth = true
        $scope.loggingin = false
        $scope.profile = data.profile
        $scope.username = data.username
        $route.reload()
      .error (data) ->
        console.log(data)

  $scope.logout = ->
    $http.get('/api/logout')
      .success (data) ->
        $scope.auth = false
        $scope.profile = null
        $scope.loginform['username'] = ''
        $scope.loginform['password'] = ''
        $location.path( "#/home" )
        $route.reload()


.controller 'UserController', ($scope, $location, $http) ->
  userform = {
    'email':'',
    'first_name': '',
    'last_name': '',
    'date_naissance': '',
    'adresse': '',
    'telephone': '',
    'password': ''
  }

  $scope.userform = {}
  _.extend($scope.userform, userform)

  $scope.submit = (restaurateur=false) ->
    $scope.userform.is_restaurateur = restaurateur
    $http.post('/api/register', $scope.userform)
      .success (data) ->
        if $location.path() == '/admin/users'
          $scope.profiles.push(data)
          if $scope.userform.resto
            $scope.options =
              (opt for opt, opt in $scope.options when opt.value != $scope.userform.resto)
            $scope.selected_resto = $scope.options[0]
          else
            alert("il est preferable d'assigner un restaurant")
          _.extend($scope.userform, userform)
        else
          alert('registration successful')
          $location.path( "#/home" );
      .error (data) ->
        console.log(data)

  if $location.path() == '/admin/users'
    $http.get('/api/all_profiles')
      .success (data) ->
        $scope.profiles = data
      .error (data) ->
        console.log(data)

    $scope.options = [{'label':'None', 'value':''}]
    $scope.selected_resto = $scope.options[0]
    $http.get('/api/all_resto')
      .success (data) ->
        $scope.restos = data
        $scope.available_resto =
        (resto for resto, resto in $scope.restos when resto.user == null)
        for resto in $scope.available_resto
          $scope.options.push({'label':resto.name, 'value':resto.pk})
      .error (data) ->
        console.log(data)
 
  $scope.edit = (profile) ->
    profile.backup = _.clone(profile)
    profile.backup.user = _.clone(profile.user)

  $scope.cancel = (profile) ->
    _.extend(profile, profile.backup);
    delete profile['backup']

  $scope.save = (profile) ->
    $http.post('/api/edit_profile', profile)
      .success (data) ->
        delete profile['backup']

  $scope.delete = (profile) ->
    $http.post('/api/delete_profile', profile)
      .success (data) ->
        $scope.profiles = _.without($scope.profiles, profile)
      .error (data) ->
        console.log(data)
