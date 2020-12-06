  $('#search_posts')
  .search({
    apiSettings: {
      url: '/api/search_posts?name={query}'
    },
    fields: {
      results : 'results',
      title   : 'title',
      description : 'content',
      content : 'content',
      url     : 'post_url',
    },
    minCharacters : 3
  });