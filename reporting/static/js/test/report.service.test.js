describe('Report', function(){
  "use strict";
var Report, $window;


  beforeEach(function(){
    module('opal.reporting');
    inject(function($injector){
      Report = $injector.get('Report');
      $window = $injector.get('$window');
    });

    spyOn($window, "open");
  });

  it('show open a window on download', function(){
      var report = new Report({download_link: "some_link"});
      report.download(false);
      expect($window.open).toHaveBeenCalledWith("some_link", '_blank');
  });
});
