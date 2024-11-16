const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

// filenames to include (without paths)
const postsFilePath = path.join(__dirname, 'posts.txt');

// Vault directory path
const postsDir = path.join(
  process.env.HOME, 
  'Library', 
  'Mobile Documents', 
  'iCloud~md~obsidian', 
  'Documents', 
  'Home', 
  //'The View From Afar'
);

// Output path for JSON file
const outputFile = path.join(__dirname, '..', 'public', 'posts.json');


const includedFiles = fs.readFileSync(postsFilePath, 'utf-8')
    .split('\n')
    .map(filename => filename.trim() + '.md')
    .filter(filename => filename);

// Recursive function to search for specified filenames
function findIncludedFiles(dir) {
  let foundFiles = [];
  const items = fs.readdirSync(dir, { withFileTypes: true });

  items.forEach(item => {
    const itemPath = path.join(dir, item.name);

    if (item.isDirectory()) {
      // Recurse into subdirectories
      foundFiles = foundFiles.concat(findIncludedFiles(itemPath));
    } else if (includedFiles.map(item => {return item.toLowerCase()}).includes(item.name.toLowerCase())) {
      // Check if filename matches the included list
      foundFiles.push(itemPath);
      console.log(`Found: ${item.name}`);
    }
  });
  return foundFiles;
}

// Read files and extract metadata
const posts = findIncludedFiles(postsDir).map(filePath => {
  const fileContents = fs.readFileSync(filePath, 'utf-8');
  const { data } = matter(fileContents);

  return {
    title: data.title || path.basename(filePath, '.md'),
    slug: path.basename(filePath, '.md'),
    date: data.date ? new Date(data.date).toISOString().split('T')[0] : null,  // Format date as YYYY-MM-DD
    tags: data.tags || []  // Extract tags if available
  };
});

// Write metadata to posts.json
fs.writeFileSync(outputFile, JSON.stringify(posts, null, 2), 'utf-8');
console.log(`Posts metadata generated successfully in ${outputFile}`);