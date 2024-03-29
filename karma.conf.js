// Karma configuration
// Generated on Thu Apr 11 2013 18:17:10 GMT-0700 (PDT)


// base path, that will be used to resolve files and exclude
basePath = '';


// list of files / patterns to load in the browser
files = [
  JASMINE,
  JASMINE_ADAPTER,
  'staticfiles/js/*.js',
  /*
  'staticfiles/js/angular.min.js',
  'staticfiles/js/app.js',
  'staticfiles/js/controllers.js',
  */
  'test-js/lib/angular-mocks.js',
  
  
  'test-js/unit/*.js'
];


// list of files to exclude
exclude = [
  
];

// proxies
proxies = {
	'/' : 'http://127.0.0.1:8000'
}

// test results reporter to use
// possible values: 'dots', 'progress', 'junit'
reporters = ['progress'];


// web server port
port = 9876;


// cli runner port
runnerPort = 8080;


// enable / disable colors in the output (reporters and logs)
colors = true;



//urlRoot = '/angular/#/public_ideas/'

// level of logging
// possible values: LOG_DISABLE || LOG_ERROR || LOG_WARN || LOG_INFO || LOG_DEBUG
logLevel = LOG_INFO;


// enable / disable watching file and executing tests whenever any file changes
autoWatch = true;


// Start these browsers, currently available:
// - Chrome
// - ChromeCanary
// - Firefox
// - Opera
// - Safari (only Mac)
// - PhantomJS
// - IE (only Windows)
browsers = ['Chrome'];


// If browser does not capture in given timeout [ms], kill it
captureTimeout = 60000;


// Continuous Integration mode
// if true, it capture browsers, run tests and exit
singleRun = false;
