# Blanton Art Recommender

## Setup

The python notebook `blanton_final_project.ipynb` requires the following prerequistes under a python 3 environment:
* jupyter notebook -- to view the notebook with formatted markdown cells.
* pandas -- to create and manipulate large matrices of data.
* mlxtend -- to provide the statistical algorithms used to create recommendations.
* numpy -- to provide simple matrix manipulation functionality that works hand-in-hand with pandas.

To quickly install these requirements, run the command: 

```console
foo@bar:~/$ pip3 install -r requirements.txt
```

Once the environment has been setup, we need to ensure that the datasets are placed in the correct directory hierarchy. The file-tree diagram below shows the structure expected by `blanton_final_project.ipynb`:

```
├── blanton_data/
│   ├── ahasbany_blanton.xlsx
│   ├── akp2597_blanton.xlsx
│   ├── akshay17_blanton.xlsx
│   ├── AnaW4804_blanton-1.xlsx
│   ├── araman18_blanton.xlsx
│   ├── ashk2016_blanton.xlsx
│   ├── ayan_blanton.xlsx
│   ├── benli_blanton.xlsx
│   ├── brandonn_blanton.xlsx
│   ├── caitlien_blanton.xlsx
│   ├── cjenwere_blanton.xlsx
│   ├── colette_blanton.xlsx
│   ├── cst774_blanton.xlsx
│   ├── ericamtz_blanton.xlsx
│   ├── Frp323_blanton-1.xlsx
│   ├── gokul_blanton.xlsx
│   ├── gperez13_blanton.xlsx
│   ├── gskaggs_blanton.xlsx
│   ├── hh26257_blanton.xlsx
│   ├── hrithikr_blanton.xlsx
│   ├── ich_blanton-1.xlsx
│   ├── jrm7328_blanton.xlsx
│   ├── kevliang_blanton.xlsx
│   ├── kjh2858_blanton.xlsx
│   ├── kjoseph_blanton.xlsx
│   ├── kushalcd_blanton.xlsx
│   ├── lgm977_blanton.xlsx
│   ├── manders_blanton.xlsx
│   ├── maram_blanton.xlsx
│   ├── mshao123_blanton-2.xlsx
│   ├── nithin13_blanton.xlsx
│   ├── nkumar_blanton.xlsx
│   ├── nzubair_blanton.xlsx
│   ├── pa8789_blanton.xlsx
│   ├── poi_blanton.xlsx
│   ├── pranooha_blanton.xlsx
│   ├── preston_blanton.xlsx
│   ├── rahulram_blanton.xlsx
│   ├── raymond_blanton.xlsx
│   ├── riz74_blanton.xlsx
│   ├── rsmoreno_blanton.xlsx
│   ├── ryanyz10_blanton.xlsx
│   ├── saomyat_blanton.xlsx
│   ├── serfurt_blanton.xlsx
│   ├── shaniyur_blanton.xlsx
│   ├── shayampat_blanton.xlsx
│   ├── simon18_blanton.xlsx
│   ├── snowaski_blanton.xlsx
│   ├── sra2398_blanton-1.xlsx
│   ├── sruthi_blanton.xlsx
│   ├── tchatter_blanton.xlsx
│   └── viswa_blanton.xlsx
└── blanton_final_project.ipynb
```

Please note that the `blanton_final_project.ipynb` and `blanton_data/` folder need to be placed on the same level. Also note that the names and number of actual `.xlsx` files provided to the recommender can be varied by adding or removing files in the `blanton_data/` directory.

## Running the recommender

To run the recommender, launch the notebook using jupyter:

```console
foo@bar:~/$ jupyer notebook blanton_final_project.ipynb
```

Once a browser window appears, navigate to the `Cell` drop-down menu and choose `Run all below`.

The recommender should output a file called `student_recommentdations.xlsx` in the same directory as the notebook. This file contains 3 recommendations per student.


# Our Process

## 1) Fixing the Accession Numbers

We started by dividing up the entire `blanton_list.xlsx` file into two. We then used Blanton's website to check the number of results when a particular row was searched. 
We automated this process, but due to the submission requirements we do not provide the code. Both of our scripts used the same process as detailed below:
1. Create a search query string by combining `Title` and `Artist Name`. 
2. Send this query to `https://collection.blantonmuseum.org/4DACTION/HANDLECGI/Search`.
3. Get the number of search results.
4. If more than 1 result was found, we manually fixed each row.
5. We fixeed the row by either adding a zero, two zeros, or just re-copying the correct `Accession #` from the website for this given item.

This yielded about 70 corrections made to `blanton_list.xlsx` that were then transfered to `blanton_list_fixed.xlsx`.

### Running the Code


For running on all fixed data and generating the `blanton_fixed_images.xlsx` file:
```
python3 blanton_image_search.py blanton_list_fixed.xlsx blanton_list_images.xlsx False
```

To run our test cases, results are put in `test_results.xlsx`:
```
python3 blanton_image_search.py blanton_test.xlsx test_results.xlsx True
```



## 2) Filter out Rows Without Digital Images

For step 2 of the project, we wrote a tool `blanton_image_search.py` that can systematically search Blanton's DB for a given art piece, parse the JSON response, and determine if the art piece has an image. 

Our program takes three arguments: 
1. The input .xlsx file: Should be the file containing the fixed `Accession #`s.
2. The output .xlsx file: The empty file that gets generated which will include all original data from `1.`, along with the boolean column representing if an item has an image.
3. Test mode: If set to `True`, will run in test mode. This will check the input file `1.` against known results. This can only be used usefully if the input file is `blanton_test.xlsx`.


Our program takes the arguments and does the following:
1. Loop over all the items in the input `.xlsx` file.
2. For each item, define an ACC object.
3. Each ACC object allows us to create the URL strings in an easy-to-manage way.
4. We then call `getJSONLink()` on the ACC object, which returns a formatted JSON query that Blanton's DB can understand. The string that gets formatted with the correct Accession Number is shown:
`https://collection.blantonmuseum.org/results.html?&layout=objects&format=json&maximumrecords=-1&recordType=objects_1&query=mfs%20all%20%22{}%22"`
5. We then use the `requests` module to send the JSON request.
6. Next, we use the `json` module to parse the result, after cleaning out any empty spaces and newline chars.
7. Finally, we check if the result has any values in the `'Images'` sub-field within the JSON response.
8. If the sub-field has more than 1 element, there is an image on Blanton's website for the item. Otherwise, there is no image.
9. During all this we keep track of which items had an image, and append the list as a column once all the rows have been checked.


The result of the above approach combined with our process during step 1 gave us 1067 items that had images. This is about 77.7% of all items.

Before using the JSON approach, we followed the instructions given on the assignment page. This method gave us very low coverage, under-reporting the number items that actually had images, with links that looked like `[Accession #].1-499.jpg`. This is one of the many cases where the links seemed random, containing numbers that had nothing to do with the item or its page (seemingly).

We then gave the JSON approach a shot and witnessed edge-case links get covered correctly.
