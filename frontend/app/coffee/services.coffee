angular.module('resto.services', ['ngResource'])

.factory 'Resto', ($resource) ->
  $resource('http://127.0.0.1:8000/api/resto/:id',
    { id: '@_id' }, {update:{method:'PUT'}})

.factory 'Profile', ($resource) ->
  $resource('http://127.0.0.1:8000/api/profile/:id',
    { id: '@_id' }, {update:{method:'PUT'}})

.factory 'Commande', ($resource) ->
  $resource('http://127.0.0.1:8000/api/commande/:id',
    { id: '@_id' }, {update:{method:'PUT'}})

