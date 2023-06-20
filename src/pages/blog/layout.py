# package imports
import dash

dash.register_page(
    __name__,
    path="/blog",
    title="Blog",
    description="This is the Fortunato Wheels blog page",
)

from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import date
import os
import frontmatter
import platform

# set file location
cwd = os.getcwd()
file_path_in = os.path.join(cwd, "src", "pages", "blog", "articles")
date_format = "%B %#d, %G" if platform.system() == "Windows" else "%B %-d, %G"


def create_article_card(post):
    """Create clickable card to navigate to the article"""
    date_str = post.get("date").strftime(date_format)
    card = dbc.Card(
        html.A(
            [
                dbc.CardImg(src=f'{post.get("image")}', top=True),
                dbc.CardBody(
                    [
                        html.H4(f'{post.get("title")}', className="card-title"),
                        html.P(f'{post.get("description")}', className="card-text"),
                    ]
                ),
                dbc.CardFooter(f'{post.get("author")} - {date_str}', class_name="mb-0"),
            ],
            href=post.get("permalink"),
            className="text-decoration-none text-body h-100 d-flex flex-column align-items-stretch",
        ),
        class_name="article-card h-100",
    )
    return card


def create_article_page(post):
    """Create the layout of the article page"""
    date_str = post.get("date").strftime(date_format)

    image = post.get("image")
    layout = html.Div(
        dbc.Row(
            dbc.Col(
                [
                    # add white space above the image
                    html.Div(style={"height": "20px"}),
                    html.Img(
                        src=f"{image}",
                        # center the image and make it 90% of the column width and have it with rounded corners and a shadow
                        style={
                            "display": "block",
                            "margin-left": "auto",
                            "margin-right": "auto",
                            "width": "100%",
                            "border-radius": "10px",
                            "box-shadow": "0px 0px 10px 0px rgba(0,0,0,0.75)",
                        },
                    ),
                    html.Div(style={"height": "20px"}),
                    html.H1(f'{post.get("title")}'),
                    html.Hr(),
                    html.P(f'{post.get("author")} - {date_str}'),
                    html.Hr(),
                    dcc.Markdown(post.content, className="markdown"),
                ],
                width={"size": 12},
                lg={"size": 8, "offset": 2},
                xl={"size": 6, "offset": 3},
            )
        ),
        className="mb-4",
    )
    return layout


# iterate over items in article page
article_cards = []
article_files = os.listdir(file_path_in)
article_files.reverse()  # reverse the list so the article show up properly

for article_name in article_files:
    # read in contents of a given article
    article_path = os.path.join(file_path_in, article_name)
    with open(article_path, "r", encoding="utf-8") as f:
        post = frontmatter.load(f)

    publish_date = post.get("date")

    # skip articles that aren't published yet or are the sample files
    if publish_date > date.today() or article_name.startswith("sample"):
        continue

    # format image for proper sharing
    sharing_image = post.get("image").lstrip("/assets/")

    # register the specific page for the article
    dash.register_page(
        post.get("title"),
        title=post.get("tab_title"),
        description=post.get("description"),
        image=sharing_image,
        path=post.get("permalink"),
        layout=create_article_page(post),
    )
    # create the article card and add it to the list of cards
    article_cards.append(create_article_card(post))


layout = html.Div(
    [
        # wrap the articles in a dbc.Col that's offset on large screens, otherwise full width
        dbc.Col(
            children=[
                html.Div(style={"height": "20px"}),
                html.H1("Fortunato Wheels Blog"),
                html.P(
                    "Welcome to the Fortunato Wheels blog! Here you'll find articles about the used car market, how to buy a used car, and more!"
                ),
                html.Hr(),
                dbc.Row(
                    [dbc.Col(c, md=6, lg=6, align="stretch") for c in article_cards],
                    class_name="g-3 my-1",
                ),
            ],
            width={"size": 12, "order": "last", "offset": 0},
            lg={"size": 8, "order": "last", "offset": 2},
        ),
        # add a placeholder vertical div of 80% vh
        html.Div(style={"height": "70vh"}),
    ]
)


# dash.register_page(
#     __name__,
#     path="/blog",
#     title="Blog",
#     description="This is a simple blog page",
#     layout=layout,
# )
