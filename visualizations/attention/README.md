# Self-attention: red toy robot

Open [index.html](index.html) in a browser. No install, server, API key, or network is needed. Keep `index.html`, `style.css`, and `app.js` together.

The eleven steps use **red toy robot** throughout: `toy` specifies a plaything and changes the interpretation of `robot`. The opening illustration shows that distinction; its shapes and colours are explanatory drawings, not model outputs or vector coordinates. Play advances the lesson and animates information flow; Back/Next and the step tabs support teaching at your own pace. The matrix panel is optional. Click a result entry to highlight its input row and matrix column; “Next product” walks through the accumulating dot product. Arrow keys move between steps; Space toggles playback when focus is outside a control. Reduced-motion preferences disable animated paths and entrances.

The calculation uses rows for token vectors, following the original Transformer paper. The toy input is `X = I₃`, with `WQ = [[1,0],[0,1],[1,1]]`, `WK = [[2,0],[0,2.3],[0,0.2]]`, and identity value/output maps. All numbers are invented teaching parameters, not weights measured from a trained model. Matrix coordinates do not literally encode the three words' meanings. Scores are `Q Kᵀ / √2`; future columns are masked before row-wise softmax; `H = A V`; the attention residual update is `X + H`. Feed-forward processing, normalization, position encoding, and multiple heads are outside the arithmetic example and are identified as omissions.

The query, key, and value maps in one attention step all take the same incoming representations. Updated representations only produce new queries/keys/values in a later block, with that block's own learned maps. The complete block's feed-forward and normalization operations intervene.

Original visual and code implementation inspired by [3Blue1Brown's attention explanation](https://www.3blue1brown.com/lessons/attention/); mathematical reference: [Attention Is All You Need](https://arxiv.org/abs/1706.03762). Linked DeepLearning.AI resources are suggestions for further study; this artifact does not reproduce their videos or graphics.
