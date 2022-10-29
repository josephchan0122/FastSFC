import _ from 'lodash';
import $ from 'jquery';
import React, { Component } from 'react';
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import F from './Formatter.jsx';

class DocumentList extends Component {
  constructor(props) {
    super(props);

    this.state = {
      data: [],
      documents: [],
      loading: true,
      error: false,
      placeholder: 'Loading...',
      ticker: window.location.pathname.split('/').pop(),
      type: props.type || '',
      limit: props.limit || 10,
      offset: props.offset || 0,
      format: props.format || 'categorized',
    };
  }

  componentDidMount() {
    if (this.state.type) {
      this.$loadMoreButton = $('.load-more-' + this.state.type);
    } else {
      this.$loadMoreButton = $('.load-more');
    }

    this.$loadMoreButton.click(this.fetch.bind(this));
  }

  fetch() {
    const params = $.param({
      format: 'json',
      ticker: this.state.ticker,
      limit: this.state.limit,
      type: this.state.type,
      offset: this.state.offset,
    });

    fetch('/api/v1/document?' + params)
      .then(res => {
        if (res.status !== 200) {
          return this.setState({
            loading: false,
            error: true,
          });
        }
        return res.json();
      })
      .then(data => {
        this.state.data = data;
        this.state.documents = _.concat(this.state.documents, data.results);
        this.state.offset += this.state.limit;

        this.setState({ loading: false });
      });
  }

  renderSuccess() {
    const { documents, data, limit, format } = this.state;

    if (!documents || !data) {
      this.renderError();
    }

    // Get market
    const market = documents[0].company.layout;

    // Increase offset
    this.state.offset += limit;

    // Decide whether or not to show load more button
    if (data.count > this.state.offset) {
      this.$loadMoreButton.show();
    } else {
      this.$loadMoreButton.hide();
    }

    // HK market
    if (market === 'hk') {
      if (format === 'categorized') {
        return (
          <React.Fragment>
            {documents.map(d => (
              <tr key={d.id}>
                <td className="ellipsis">{F.date(d.date)}</td>
                <td className="ellipsis">
                  <a href={'/document/' + d.id}>{d.description}</a>
                </td>
              </tr>
            ))}
          </React.Fragment>
        );
      }

      return (
        <React.Fragment>
          {documents.map(d => (
            <tr key={d.id}>
              <td className="ellipsis">{F.date(d.date)}</td>
              <td className="ellipsis">{F.capitalize(d.cat.type)}</td>
              <td className="ellipsis">
                <a href={'/document/' + d.id}>{d.description}</a>
              </td>
            </tr>
          ))}
        </React.Fragment>
      );
    }

    // US market
    if (format === 'categorized') {
      return (
        <React.Fragment>
          {documents.map(d => (
            <tr key={d.id}>
              <td className="ellipsis">{F.date(d.date)}</td>
              <td className="ellipsis">{d.cat.name}</td>
              <td className="ellipsis">
                <a href={'/document/' + d.id}>{d.description}</a>
              </td>
            </tr>
          ))}
        </React.Fragment>
      );
    }

    return (
      <React.Fragment>
        {documents.map(d => (
          <tr key={d.id}>
            <td className="ellipsis">{F.date(d.date)}</td>
            <td className="ellipsis">{F.capitalize(d.cat.name)}</td>
            <td className="ellipsis">
              <a href={'/document/' + d.id}>{d.description}</a>
            </td>
          </tr>
        ))}
      </React.Fragment>
    );
  }

  renderError() {
    return <p>{this.state.placeholder}</p>;
  }

  render() {
    if (this.state.loading) {
      return <React.Fragment />;
    }
    if (this.state.error) {
      return this.renderError();
    }
    return this.renderSuccess();
  }
}

DocumentList.propTypes = {
  type: PropTypes.string,
  format: PropTypes.oneOf(['categorized', 'chronological']),
  offset: PropTypes.number,
  limit: PropTypes.number,
};

export default hot(module)(DocumentList);
