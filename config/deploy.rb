# config valid only for current version of Capistrano
lock '3.6.1'

set :application, 'spotify_classify'
set :repo_url, 'git@github.com:YeasterEgg/spotify_classify.git'
set :deploy_to, '/var/www/spotify_classify'
set :log_level, :info
set :keep_releases, 2

role :app, "46.101.114.92"
role :web, "46.101.114.92"

set :branch, ENV["BRANCH"] || 'master'

set :scm, :git
