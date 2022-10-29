import _ from 'lodash';
import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';
import DocumentList from './components/DocumentList.jsx';
import DocumentDetail from './components/DocumentDetail.jsx';
import Search from './components/Search';
import Settings from './components/Settings';
import Watch from './components/Watch';

const profileDropdown = document.getElementById('profile-dropdown');
if (profileDropdown !== null) {
  const $toggle = $('#profile-dropdown .dropdown-toggle');
  const $el = $(profileDropdown);
  $toggle.click(() => {
    $el.toggleClass('open');
  });
}

const inputSearch = document.getElementById('input-search');
if (inputSearch !== null) {
  ReactDOM.render(<Search />, inputSearch);
}

const watch = document.getElementById('watch-button');
if (watch !== null) {
  ReactDOM.render(<Watch />, watch);
}

const settings = document.getElementById('settings');
if (settings !== null) {
  ReactDOM.render(<Settings />, settings);
}

const documentDetail = document.getElementById('document-detail');
if (documentDetail !== null) {
  ReactDOM.render(<DocumentDetail type="document" />, documentDetail);
}

const websiteDocumentDetail = document.getElementById(
  'website-document-detail'
);
if (websiteDocumentDetail !== null) {
  ReactDOM.render(
    <DocumentDetail type="websiteDocument" />,
    websiteDocumentDetail
  );
}

const documentFinancialChronoLoader = document.getElementById(
  'document-financials-chrono-loader'
);
if (documentFinancialChronoLoader !== null) {
  ReactDOM.render(
    <DocumentList offset={20} limit={20} format="chronological" />,
    documentFinancialChronoLoader
  );
}

// Render document loader for each type
const types = [
  'financials',
  'announcements',
  'ownership',
  'prospectuses',
  'proxies',
  'other',
];

_.each(types, type => {
  const el = 'document-' + type + '-loader';
  const node = document.getElementById(el);
  const f = 'categorized';

  if (node !== null) {
    ReactDOM.render(<DocumentList type={type} offset={8} format={f} />, node);
  }
});
