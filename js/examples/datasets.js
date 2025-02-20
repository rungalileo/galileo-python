import 'dotenv/config';
import pkg from '@galileo/ts-sdk';

const { getDatasets, createDataset, getDatasetContent } = pkg;

// Create a dataset
const dataset = await createDataset(
  {
    col1: [1, 2, 3],
    col2: ['a', 'b', 'c']
  },
  'My dataset'
);
console.log('Created dataset:', dataset);

// Get all datasets
console.log('Listing datasets...');
const datasets = await getDatasets();
datasets.forEach((dataset) => console.log(dataset));

// Get dataset content
const content = await getDatasetContent(dataset.id);
console.log('Dataset content:', content);
