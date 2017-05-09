angular.module('opal.reporting').factory('Report', function($window){
  var Report = function(reportDefinition){
    _.extend(this, reportDefinition);
    this.async_waiting = false;
  };

  Report.prototype = {
    download: function(asynchronously){
      this.async_waiting = true;
      $window.open(this.download_link, '_blank');
    }
  };

  return Report;
});
