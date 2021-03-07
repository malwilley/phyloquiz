<footer>
  <div>
    <strong>PhyloQuiz</strong> is an experimental quiz generator for educators,
    biology nerds, or anyone who enjoys wasting time. See my other work at
    <a href="https://malachi.dev/" target="_blank" rel="noopener noreferrer"
      >malachi.dev</a
    >, or view the
    <a
      href="https://github.com/malwilley/phyloquiz"
      target="_blank"
      rel="noopener noreferrer">source code</a
    > on GitHub.
  </div>
  <hr />
  <div>
    Huge thanks to the team at <a
      href="http://www.onezoom.org/"
      target="_blank"
      rel="noopener noreferrer">OneZoom</a
    > for providing access to their comprehensive dataset and for their continued
    interest in this project. Go to their site and sponser a leaf to keep them running!
  </div>
</footer>

<style lang="scss">
  @import 'src/css/variables';

  footer {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 3rem 2rem;
    background: $primary-20;
    border-top: 1px solid rgba($primary-60, 0.1);

    font-size: $sans-serif-size-small;
    line-height: 1.5;
    font-family: $sans-serif-font;

    div {
      max-width: 26rem;
    }
  }

  hr {
    width: 1rem;
    background-color: $text-color-light;
  }
</style>
