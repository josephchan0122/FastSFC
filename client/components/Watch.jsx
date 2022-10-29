import React from 'react';
import { hot } from 'react-hot-loader';

/**
 * Company watch component.
 */
class Watch extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      /**
       * Current watching status
       */
      status: null,
    };
    /**
     * Common headers
     */
    this.headers = {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': this.getCookie('csrftoken'),
    };
    /**
     * Api endpoint base url
     */
    this.url = '/api/v1/watchlist/';
    /**
     * An enum with possible statuses
     */
    this.statuses = {
      CAN_WATCH: 'can_watch',
      WATCHED: 'watched',
      LOGIN_REQUIRED: 'login_required',
    };
    /**
     * Current company's ticker
     */
    this.ticker = window.location.href
      .split('/')
      .filter(i => i)
      .pop();
  }

  /**
   * Run a HEAD request to check  if user is watching already
   */
  componentWillMount() {
    fetch(this.url + this.ticker + '/', {
      method: 'HEAD',
      headers: this.headers,
      credentials: 'same-origin',
    })
      .then(response => {
        switch (response.status) {
          case 200:
            this.setState(() => ({ status: this.statuses.WATCHED }));
            break;
          case 404:
            this.setState(() => ({ status: this.statuses.CAN_WATCH }));
            break;
          case 403:
            this.setState(() => ({ status: this.statuses.LOGIN_REQUIRED }));
            break;
          default:
            break;
        }
      })
      .catch();
  }

  /**
   * helper to get required cookies
   */
  getCookie = name => {
    if (!document.cookie) {
      return null;
    }

    const xsrfCookies = document.cookie
      .split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));

    if (xsrfCookies.length === 0) {
      return null;
    }

    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
  };

  /**
   * Main handler of this component
   * All logic for watching/unwatching/redirection is here
   */
  handleClick = e => {
    e.preventDefault();
    switch (this.state.status) {
      case this.statuses.WATCHED:
        // is user is watching already, remove db entry
        fetch(this.url + this.ticker + '/', {
          method: 'DELETE',
          headers: this.headers,
          credentials: 'same-origin',
        })
          .then(response => {
            switch (response.status) {
              case 204:
                // ok, entry was removed
                this.setState(() => ({ status: this.statuses.CAN_WATCH }));
                break;
              case 404:
                // something is wrong
                this.setState(() => ({ status: this.statuses.WATCHED }));
                break;
              case 403:
                // user should login
                this.setState(() => ({ status: this.statuses.LOGIN_REQUIRED }));
                break;
              default:
                break;
            }
          })
          .catch();
        break;
      case this.statuses.CAN_WATCH:
        // user wants to watch
        fetch(this.url, {
          method: 'POST',
          headers: this.headers,
          credentials: 'same-origin',
          body: JSON.stringify({ company: this.ticker }),
        })
          .then(response => {
            switch (response.status) {
              case 200:
                // ok, user is watching now
                this.setState(() => ({ status: this.statuses.WATCHED }));
                break;
              case 404:
                // wrong request, ticker doesn't exist
                this.setState(() => ({ status: this.statuses.CAN_WATCH }));
                break;
              case 403:
                // should login
                this.setState(() => ({ status: this.statuses.LOGIN_REQUIRED }));
                break;
              default:
                break;
            }
          })
          .catch();
        this.setState(() => ({ status: this.statuses.WATCHED }));
        break;
      case this.statuses.LOGIN_REQUIRED:
        // redirect user to the login page
        window.location =
          window.location.origin + '/login/?next=' + window.location.pathname;
        break;
      default:
        break;
    }
  };

  render() {
    let className = 'btn btn-watchlist';
    let label = 'Watch';

    switch (this.state.status) {
      case this.statuses.WATCHED:
        className += ' active';
        label = 'Watching';
        break;
      case this.statuses.CAN_WATCH:
        break;
      case this.statuses.LOGIN_REQUIRED:
        break;
      default:
        break;
    }

    return (
      <button onClick={this.handleClick} className={className} type="button">
        <i className="fa fa-eye fa-sm" aria-hidden="true" /> {label}
      </button>
    );
  }
}

export default hot(module)(Watch);
