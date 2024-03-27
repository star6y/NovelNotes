## App Info:

* App Name: NovelNotes
* App Link: [Link](https://project-1-ice-water.onrender.com/)


## Key Features

* Used the [Google Books API](https://developers.google.com/books/docs/overview) to load information about books and support book search.
* Implemented an up/down voting system, as well as comments to support interactivity with book reviews.
* New book recommendations based on a user's preferences, infered from their review history.


## Testing Notes

1. You can upload a custom pfp by going to `Profile` > `Clicking your PFP`
2. Google's Book API does not feature deterministic ordering for searches. When you refresh book search, the order may change. Unfortunately there is no configuration that solves this, setting the order by parameter in the API did not resolve this.



## Screenshots of Site


### Home page
<img width="2056" alt="image" src="https://github.com/csci5117s24/project-1-ice-water/assets/66842958/85f968cf-8604-4098-9574-8519054c80f5">

### Book page
<img width="2056" alt="image" src="https://github.com/csci5117s24/project-1-ice-water/assets/66842958/3d7ac7bc-dc91-4283-8133-50f33a0e3d45">

### Profile page
<img width="2056" alt="image" src="https://github.com/csci5117s24/project-1-ice-water/assets/66842958/774d10c4-2f22-4da9-919d-3b01c95e5f9e">

### Search page (Books)
<img width="2056" alt="image" src="https://github.com/csci5117s24/project-1-ice-water/assets/66842958/f025cb30-d850-4a0e-906b-59fe857e9c07">

### Search page (Users)
<img width="2056" alt="image" src="https://github.com/csci5117s24/project-1-ice-water/assets/66842958/84c38cad-ba33-4899-8a32-02ad26c02d51">

### About page
<img width="2056" alt="image" src="https://github.com/csci5117s24/project-1-ice-water/assets/66842958/6812fd01-eac1-43ed-a5ba-db4973234790">

### Discover / Recommend a book page
<img width="2056" alt="image" src="https://github.com/csci5117s24/project-1-ice-water/assets/66842958/6cb710f6-7e56-4e59-8121-d36be1586835">


## Mock-up 

Figma link for the project can be found [here](https://www.figma.com/file/n4dmQgEKiddR8WksucwFnY/WireFrameV2?type=design&node-id=0%3A1&mode=design&t=GnHRJtFsscTpLNui-1).

## [1]
### Overview, contains all pages and anticipated links between pages.
<img width="1511" alt="image" src="https://github.com/csci5117s24/project-1-ice-water/assets/66842958/a3fccfa9-d3a6-46ef-a7e6-9d664ccac64a">

## [2] 
### Home page - contains featured books and reviewers
### About page - contains info about the project
<img width="661" alt="image" src="https://github.com/csci5117s24/project-1-ice-water/assets/66842958/2dd8a40c-fec1-4866-8471-862f76a47595">

## [3]
### User search results (left) - Contains the result of a user search. Users are displayed in a grid.
### Book search results (right) - Contains the result of a book search. Books are displayed in a grid with title, image, and rating.
<img width="1513" alt="image" src="https://github.com/csci5117s24/project-1-ice-water/assets/66842958/0955409e-d38e-451b-a39e-4e5c38f6de10">

## [4]
### User Profile screen - contains a user's reviews and comments
<img width="835" alt="image" src="https://github.com/csci5117s24/project-1-ice-water/assets/66842958/8e53b006-1048-4247-b945-17727ba9022a">

## [5]
### view page (left) - Displays book info and reviews
### Comment popup (right) - displays the comments under a review
<img width="1133" alt="image" src="https://github.com/csci5117s24/project-1-ice-water/assets/66842958/696ddcea-954e-41d8-ab56-803d90437dbd">


## External Dependencies

**Document integrations with 3rd Party code or services here.
Please do not document required libraries. or libraries that are mentioned in the product requirements**

* [Google Books API V1](https://developers.google.com/books/docs/overview): Used to fetch and search books
* [Gravatar](https://gravatar.com/): Used to provide unique default profile pictures
* [OpenAI Chat Completions API](https://platform.openai.com/docs/guides/text-generation/chat-completions-api): Used to create book recommendations

**If there's anything else you would like to disclose about how your project
relied on external code, expertise, or anything else, please disclose that
here:**

...
