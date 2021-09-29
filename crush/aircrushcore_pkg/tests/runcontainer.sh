container="library://dmattie/default/image:sha256.5146a3230920d96f5b1f0ed97ada6b6ff0545acb36b1841a31250893791af380"
UUID=$(cat /proc/sys/kernel/random/uuid)
#image=$( echo "$container"| cut -d: -f3 );[ ! -f "$SINGULARITY_CACHEDIR/cache/library/${image}" ] && {
singularity pull image_${UUID}.sif $container
    #}