redis-cli
ACL SETUSER redis_dev on >redis_pwd
ACL SETUSER redis_dev password "redis_pwd" >password
ACL SETUSER redis_dev +@all +@admin -@dangerous +info
ACL SAVE
AUTH redis_dev redis_pwd
