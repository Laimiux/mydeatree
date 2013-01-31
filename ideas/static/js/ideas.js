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
		urlRoot : IDEA_API,
		parse : function(data) {
			return data.objects;
		}
	});

	window.IdeaView = Backbone.View.extend({
		tagName : 'div',
		className : 'well',

		render : function() {
			// Compile the template using Handlebars
			var template = Handlebars.compile($("#private_idea_template").html());
		
			
			
			
			$(this.el).html(template(this.model.toJSON()));
			// + " " + this.model.text + " created on " + this.model.created_date);
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

		render : function() {
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
		count : function() {
			return this.ideas.length;
		},
	});

	window.app = new App();
})();

