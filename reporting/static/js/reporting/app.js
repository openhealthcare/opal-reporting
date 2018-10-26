//
// Main OPAL Reporting plugin application!
//
var opalshim = OPAL.module('opal', [])

var app = OPAL.module('opal.reporting', [
    'ngRoute',
    'ngProgressLite',
    'ngCookies',
    'opal.filters',
    'opal.services',
    'opal.directives',
    'opal.controllers',
    'opal.services'
]);

OPAL.run(app);
app.config(function($routeProvider){
  $routeProvider.when('/', {redirectTo: '/list'})
    .when('/list', {
        controller: 'ReportListCtrl',
        resolve: {},
        templateUrl: '/reporting/list'
    })
    .when('/:report', {
        controller: 'ReportDetailCtrl',
        resolve: {
            reportDefinition: function($route, reportDefinitionLoader){
              return reportDefinitionLoader.load($route.current.params.report);
            }
        },
        templateUrl: function(params){
          return "/reporting/detail/" + params.report;
        }
    });
});
