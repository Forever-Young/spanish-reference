-- EPUB needs well-formed XHTML: turn raw <br> tags from the Markdown source into real line breaks.
function RawInline(el)
  if el.format:match('html') and el.text:match('^<br%s*/?>$') then
    return pandoc.LineBreak()
  end
end
