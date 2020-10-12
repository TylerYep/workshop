set directory "large_runs"
mkdir $directory
for line in (git log --date=format:"%Y-%m-%d:%H:%m:%s" --pretty=format:"%H %ad" -100)
    echo $line | read commit date
    git checkout $commit
    cat const_override.py >> ./src/const.py
    sed -i "" "s/200/100/" profiler.py
    python profiler.py > ./$directory/$date-$commit.txt
    git stash
end