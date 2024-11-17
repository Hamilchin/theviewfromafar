const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');
const { marked } = require('marked');

// filenames to include (without paths)
const postsFilePath = path.join(__dirname, 'posts.txt');

// Vault directory path
const postsDir = path.join(
  process.env.HOME, 
  'Library', 
  'Mobile Documents', 
  'iCloud~md~obsidian', 
  'Documents', 
  'Home'
);

// Output paths
const outputFile = path.join(__dirname, '..', 'public', 'posts.json');
const postsHtmlDir = path.join(__dirname, '..', 'public', 'posts');

// Ensure the HTML directory exists
if (!fs.existsSync(postsHtmlDir)) {
  fs.mkdirSync(postsHtmlDir, { recursive: true });
}

// Recursive function to search for specified filenames
function findIncludedFiles(dir) {
  let foundFiles = [];
  const items = fs.readdirSync(dir, { withFileTypes: true });

  items.forEach(item => {
    const itemPath = path.join(dir, item.name);

    if (item.isDirectory()) {
      foundFiles = foundFiles.concat(findIncludedFiles(itemPath));
    } else if (includedFiles.map(item => item.toLowerCase()).includes(item.name.toLowerCase())) {
      foundFiles.push(itemPath);
      console.log(`Found: ${item.name}`);
    }
  });
  return foundFiles;
}

// Read posts.txt for files to include
const includedFiles = fs.readFileSync(postsFilePath, 'utf-8')
  .split('\n')
  .map(filename => filename.trim() + '.md')
  .filter(filename => filename);

//at this point, includedFiles is a list of paths

const slugToPath = new Map();


// Read files and extract metadata
const posts = findIncludedFiles(postsDir).map(filePath => {
  const fileContents = fs.readFileSync(filePath, 'utf-8');
  const { content, data } = matter(fileContents);

  const slug = path.basename(filePath, '.md')

  slugToPath.set(slug, filePath);

  if (!data.title) {
    console.warn(`Warning: Missing title in file ${filePath}`);
  }
  if (!data.written) {
    console.warn(`Warning: Missing written date in file ${filePath}`);
  }
  if (!data.edited) {
    console.warn(`Warning: Missing edited date in file ${filePath}`);
  }
  if (!data.tags || data.tags.length === 0) {
    console.warn(`Warning: Missing tags in file ${filePath}`);
  }

  return {
    title: data.title || slug,
    slug: slug,
    written: data.written ? new Date(data.written).toISOString().split('T')[0] : null, // Format date as YYYY-MM-DD
    edited: data.edited ? new Date(data.edited).toISOString().split('T')[0] : null, // Format date as YYYY-MM-DD
    tags: data.tags || [] // Extract tags if available
  };
});

function postListToMap(posts) {
  // Create a Map to organize posts by the first tag
  const postsByTag = new Map();

  // Populate the Map
  posts.forEach(post => {
    if (post.tags.length > 0) {
      const firstTag = post.tags[0]; // Take the first tag
      if (!postsByTag.has(firstTag)) {
        postsByTag.set(firstTag, []); // Initialize list if tag doesn't exist
      }
      postsByTag.get(firstTag).push(post); // Add post to the list
    }
  });

  postsByTag.forEach((postsList, tag) => {
    postsByTag.set(tag, postsList.sort((a, b) => new Date(b.written) - new Date(a.written)));
  });

  return postsByTag; 
}

const postMap = postListToMap(posts)
const mapAsObject = Object.fromEntries(postMap.entries());

// Write metadata to posts.json
fs.writeFileSync(outputFile, JSON.stringify(mapAsObject, null, 2), 'utf-8');
console.log(`Posts metadata generated successfully.`);



function generateHtml({ curPost, content, prevPost, nextPost }) {
  return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>${curPost.title}</title>
        <link rel="stylesheet" href="../blogpost.css">
    </head>
    <body>
        <div class="container">
            <h1>${curPost.title}</h1>
            <h2 class="dates">written ${curPost.written}, last edited ${curPost.edited}</h2>
            <br>

            <div class="content">
                ${content}
            </div>
            
            <nav>
                ${prevPost ? `<a href="${prevPost.slug}.html"><= </a>` : ""}
                <span></span>
                <a class="home" href="../index.html">Home</a>
                <span></span>
                ${nextPost ? `<a href="${nextPost.slug}.html"> =></a>` : ""}
            </nav>


        </div>
    </body>
    </html>`;
}

// Create HTML files and link posts within each category
postMap.forEach((postsList, tag) => {
  // Iterate through the sorted posts for this tag
  postsList.forEach((post, index) => {
    const prevPost = postsList[index - 1] || null; // Previous post or null
    const nextPost = postsList[index + 1] || null; // Next post or null

    const fileContents = fs.readFileSync(slugToPath.get(post.slug), 'utf-8');
    const { content } = matter(fileContents);
    const htmlContent = marked(content, { breaks: true, gfm: true }); // Convert Markdown to HTML

    const postHtml = generateHtml({
      curPost: post,
      content: htmlContent,
      prevPost,
      nextPost,
    });

    const outputHtmlPath = path.join(postsHtmlDir, `${post.slug}.html`);
    fs.writeFileSync(outputHtmlPath, postHtml, 'utf-8');
  });
});


console.log(`Posts HTML generated successfully.`);
