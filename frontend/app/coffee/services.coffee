angular.module('resto.prod', [])
.constant('conf',{url:'http://ram.mdupuis.com/api/'})

angular.module('resto.dev', [])
.constant('conf',{url:'http://127.0.0.1:8000/api/'})

angular.module('resto.services', ['ngResource', 'resto.dev'])
.factory 'Resto', ($resource, conf) ->
  $resource(conf.url+'resto/:id',
    { id: '@_id' }, {update:{method:'PUT'}})

.factory 'Profile', ($resource, conf) ->
  $resource(conf.url + 'profile/:id',
    { id: '@_id' }, {update:{method:'PUT'}})

.factory 'Commande', ($resource, conf) ->
  $resource(conf.url + 'commande/:id',
    { id: '@_id' }, {update:{method:'PUT'}})

