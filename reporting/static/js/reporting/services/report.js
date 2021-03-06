angular.module('opal.services').factory('Report', function($window, $interval, $http){
  "use strict";
  var Report = function(reportDefinition, criteria){
    this.reset();
    _.extend(this, reportDefinition);
    this.criteria = criteria;
  };

  Report.prototype = {
    reset: function(){
      this.asyncWaiting = false;
      this.asyncReady = false;
      this.reportStatusUrl = null;
      this.reportFileUrl = null;
    },
    downloadAsynchronously: function(){
        $window.open(this.reportFileUrl, '_blank');
    },
    startAsynchronousTask: function(){
      var self = this;
      this.asyncWaiting = true;
      $http.post(
        this.create_async_link, {criteria: JSON.stringify(self.criteria)}
      ).then(function(result){
        self.reportStatusUrl = result.data.report_status_url;
        self.reportFileUrl = result.data.report_file_url;
        self.interval = $interval(_.bind(self.getAsyncStatus, self), 1000);
      });
    },
    getAsyncStatus: function(){
      var self = this;
      $http.get(this.reportStatusUrl).then(function(result){
        if(result.data.ready){
          self.asyncReady = true;
          self.asyncWaiting = false;
          $interval.cancel(self.interval);
        }
      });
    }
  };

  return Report;
});
