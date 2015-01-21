module.exports = function(grunt){
  pkg: grunt.file.readJSON('package.json'),

  grunt.initConfig({
    coffee: {
      app: {
        files: [{
          expand: true,
          cwd: 'application/resto/static/coffee/',
          src: ['*.coffee','!.#*'],
          dest: 'application/resto/static/js/',
          ext: '.js'
        }]
      }
    },
    watch :{
      app: {
        files: ['**/*.coffee'],
        tasks: ['coffee'],
        options: {
          spawn: false,
        },
      },
    }
  });
  grunt.loadNpmTasks('grunt-contrib-coffee')
  grunt.loadNpmTasks('grunt-contrib-watch')
  grunt.registerTask('default', ['watch'])
};
