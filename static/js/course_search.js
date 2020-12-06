  $('#search_courses')
  .search({
    apiSettings: {
      url: '/api/courses?name={query}'
    },
    fields: {
      results : 'results',
      title   : 'name',
      url     : 'course_url',
      image   : 'image_url',
    },
    minCharacters : 3
  });

