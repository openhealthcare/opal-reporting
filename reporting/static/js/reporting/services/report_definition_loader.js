angular.module('opal.services')
  .factory('reportDefinitionLoader', function($q, $route, $http, $window){
    "use strict";
    return {
      load: function(reportSlug){
  	    var deferred = $q.defer();
        var url = '/api/v0.1/reporting/' + reportSlug + "/";

        $http({ cache: true, url: url, method: 'GET'}).then(
          function(resource) {
  		        deferred.resolve(resource.data);
          },
          function() {
  	        // handle error better
  	        $window.alert('Report could not be loaded');
          }
        );
  	    return deferred.promise;
      }
    };
});
