var app = app || {}; 

(function() {
	var IdeaList = Backbone.Collection.extend({
		url : IDEA_API,
		model: app.Idea,
		parse : function(data) {
			return data.objects;
		},
	});
	
	// Create our global collection of **Todos**.
	app.Ideas = new IdeaList();
}());
