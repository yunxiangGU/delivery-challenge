This is a mock data loader plugin in Python fetching news article data from New York Times API

## Getting Started

- In the project directory, run `pip install -r requirements.txt` to install the dependencies
- Simply run `delivery_challenge.py` to see the console output

## Result

- Should be able to see console output with 
  - batch number
  - batch size
  - article id
  - article headline


## Discussion and Future Work

- Only midified `getDataBatch` as that is the only `TODO` 
- `idx` in `enumerate` is zero-indexed, so output says "0 Batch of 10 items", which is not natural to read
- NY Times API key is now hard-coded with my personal API key
- Query word is also hard-coded, should find a way to initialize `NYTimesSource` class with query word, and have that as an attribute of the class
- Should implement connect and disconnect logic in a real use case
- Not sure `getSchema` should be hard-coded or parsed from the API fetch result. If the latter, then schema is not useful in validating the data (since it's from the data itself)?
- Have flattened the response dicitonaries as much as possible, but each dictionary comes with lists, so cannot be completely flat (1 level depth), unless we drop these fields such as `multimedia`, `keywords`, and `person`
