var app = app || {};

(function() {
	'use strict';

	// Todo Router
	// ----------

	var Workspace = Backbone.Router.extend({
		routes:{
			'parent/:id/#': 'setParent',
			'*default': 'defaultRoute',
		},
		
		setParent: function( id ) {
			window.app.ParentIdea = id
			//window.app.ParentIdea = param.trim() || '';
			console.log(window.app.ParentIdea);
			//console.log(param.id)
			
			window.app.Ideas.trigger('parent-change');
		},
		
		defaultRoute: function(param) {
			window.app.ParentIdea = ''
			
			window.app.Ideas.trigger('default')	
		},

		setFilter: function( param ) {
			// Set the current filter to be used
			window.app.TodoFilter = param.trim() || '';

			// Trigger a collection filter event, causing hiding/unhiding
			// of Todo view items
			window.app.Ideas.trigger('filter');
		}
	});

	app.IdeaRouter = new Workspace();
	Backbone.history.start();

}());