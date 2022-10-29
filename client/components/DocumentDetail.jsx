import React, { Component } from 'react';
import { hot } from 'react-hot-loader';
import PropTypes from 'prop-types';
import F from './Formatter.jsx';

class DocumentDetail extends Component {
  static handleBack() {
    window.history.go(-1);
    return false;
  }

  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      error: false,
      type: props.type || 'document',
    };
  }

  componentDidMount() {
    this.fetch();
  }

  fetch() {
    this.id = window.location.pathname.split('/').pop();
    this.endpoint =
      this.state.type === 'document'
        ? '/api/v1/document/'
        : '/api/v1/website-document/';

    fetch(this.endpoint + this.id + '?format=json')
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
        this.setState({ loading: false });
      });
  }

  renderSuccess() {
    const { data } = this.state;
    const filetype = data.url.split('.').pop();
    const isMobile = window.matchMedia('(max-device-width: 768px)').matches;
    let { url } = data;

    if (
      data.company.exchange === 'NYSE' ||
      data.company.exchange === 'NASDAQ' ||
      data.company.exchange === 'AMEX' ||
      data.company.exchange === 'US'
    ) {
      // for US documents
      url = (data.meta && data.meta[1].cached_url) || url;
    } else {
      // for HK documents
      url = (data.meta && data.meta[filetype.toLowerCase()]) || url;
    }

    let fileLoader = <iframe autoFocus title={url} src={url} />;

    if (filetype.toLowerCase() === 'pdf') {
      fileLoader = (
        <object data={url} type="application/pdf">
          <embed autoFocus src={url} type="application/pdf" />
        </object>
      );
    }

    return (
      <React.Fragment>
        <div
          className="left"
          style={{ height: isMobile ? 'auto' : window.innerHeight }}>
          <a href="/">
            <img alt="FastSFC" src="/static/img/logo-dark.png" />
          </a>
          <div className="back">
            <a
              role="button"
              tabIndex="0"
              onClick={DocumentDetail.handleBack}
              onKeyUp={DocumentDetail.handleBack}>
              <i className="fa fa-chevron-left" /> Back
            </a>
          </div>
          <div className="snapshot">
            <h1>{data.description}</h1>
            <div className="description">
              <span>{data.company.short_name}</span>
              <span>{data.company.exchange + ':' + data.company.ticker}</span>
              <span>{F.date(data.date)}</span>
            </div>
            <div className="actions">
              <a href={data.url} _target="blank">
                <i className="fa fa-external-link" /> Link to Original File
              </a>
            </div>
          </div>
        </div>
        <div className="right" style={{ height: window.innerHeight }}>
          {fileLoader}
        </div>
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

DocumentDetail.propTypes = {
  type: PropTypes.string,
};

export default hot(module)(DocumentDetail);
