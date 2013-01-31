/**
 * @author Laimonas Turauskas
 */

// Load the application once the DOM is ready, using `jQuery.ready`:
(function() {

	// Idea Model
	// ----------
	window.Idea = Backbone.Model.extend({
		url : function() {
			return this.get('resource_uri') || this.collection.url
		}
	});

	window.IdeaList = Backbone.Collection.extend({
		urlRoot: IDEA_API,
		model: Idea,
		parse: function(data) {
			return data.objects;
		}
	});

	/*
	 // The collection of ideas is backed by *remote server*
	 var IdeaList = Backbone.Collection.extend({
	 url: IDEA_API,
	 // Reference to this collection's model
	 model: Idea,
	 maybeFetch: function(options) {
	 // Helper function to fetch only if this collection has not been fetched before.
	 if(this._fetched) {
	 // If this has already been fetched, call the success, if it exists
	 options.success && option.success();
	 return;
	 }
	 }

	 });
	 */

	window.IdeaView = Backbone.View.extend({
		tagName : 'li',
		className : 'idea',
		

		render : function() {
			$(this.el).html(this.model.get('title') + " " + this.model.get('text') + " created on " + this.model.get('created_date')); // + " " + this.model.text + " created on " + this.model.created_date);
			return this;
		}
	});

	window.App = Backbone.View.extend({
		el : $('#app'),

		events : {
			'click .idea' : 'createIdea'
		},

		initialize : function() {
			_.bindAll(this, 'addOne', 'addAll', 'render');
			this.ideas = new IdeaList();
			this.ideas.bind('add', this.addOne);
			this.ideas.bind('refresh', this.addAll);
			this.ideas.bind('all', this.render);
			this.ideas.fetch();
		},
		
		
		render: function() {
			this.addAll();
		},

		addAll : function() {
			this.ideas.each(this.addOne);
		},

		addOne : function(idea) {
			var view = new IdeaView({
				model : idea
			});
			this.$('#ideas').append(view.render().el);
		},

		createIdea : function() {
			var title = this.$('#title').val();
			var text = this.$('#text').val();
			if (title && text) {
				this.ideas.create({
					title : title,
					text : text
				});

				this.$('#title').val('')
				this.$('#text').val('')
			}
		},
		count: function() {
			return this.ideas.length;
		},

				
	});


	window.app = new App();
})();

