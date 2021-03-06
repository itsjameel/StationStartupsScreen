"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var _a, _b;
var escape_html_1 = __importDefault(require("escape-html"));
var rich_text_types_1 = require("@contentful/rich-text-types");
var defaultNodeRenderers = (_a = {},
    _a[rich_text_types_1.BLOCKS.PARAGRAPH] = function (node, next) { return "<p>" + next(node.content) + "</p>"; },
    _a[rich_text_types_1.BLOCKS.HEADING_1] = function (node, next) { return "<h1>" + next(node.content) + "</h1>"; },
    _a[rich_text_types_1.BLOCKS.HEADING_2] = function (node, next) { return "<h2>" + next(node.content) + "</h2>"; },
    _a[rich_text_types_1.BLOCKS.HEADING_3] = function (node, next) { return "<h3>" + next(node.content) + "</h3>"; },
    _a[rich_text_types_1.BLOCKS.HEADING_4] = function (node, next) { return "<h4>" + next(node.content) + "</h4>"; },
    _a[rich_text_types_1.BLOCKS.HEADING_5] = function (node, next) { return "<h5>" + next(node.content) + "</h5>"; },
    _a[rich_text_types_1.BLOCKS.HEADING_6] = function (node, next) { return "<h6>" + next(node.content) + "</h6>"; },
    _a[rich_text_types_1.BLOCKS.EMBEDDED_ENTRY] = function (node, next) { return "<div>" + next(node.content) + "</div>"; },
    _a[rich_text_types_1.BLOCKS.UL_LIST] = function (node, next) { return "<ul>" + next(node.content) + "</ul>"; },
    _a[rich_text_types_1.BLOCKS.OL_LIST] = function (node, next) { return "<ol>" + next(node.content) + "</ol>"; },
    _a[rich_text_types_1.BLOCKS.LIST_ITEM] = function (node, next) { return "<li>" + next(node.content) + "</li>"; },
    _a[rich_text_types_1.BLOCKS.QUOTE] = function (node, next) { return "<blockquote>" + next(node.content) + "</blockquote>"; },
    _a[rich_text_types_1.BLOCKS.HR] = function () { return '<hr/>'; },
    _a[rich_text_types_1.INLINES.ASSET_HYPERLINK] = function (node) { return defaultInline(rich_text_types_1.INLINES.ASSET_HYPERLINK, node); },
    _a[rich_text_types_1.INLINES.ENTRY_HYPERLINK] = function (node) { return defaultInline(rich_text_types_1.INLINES.ENTRY_HYPERLINK, node); },
    _a[rich_text_types_1.INLINES.EMBEDDED_ENTRY] = function (node) { return defaultInline(rich_text_types_1.INLINES.EMBEDDED_ENTRY, node); },
    _a[rich_text_types_1.INLINES.HYPERLINK] = function (node, next) { return "<a href=\"" + node.data.uri + "\">" + next(node.content) + "</a>"; },
    _a);
var defaultMarkRenderers = (_b = {},
    _b[rich_text_types_1.MARKS.BOLD] = function (text) { return "<b>" + text + "</b>"; },
    _b[rich_text_types_1.MARKS.ITALIC] = function (text) { return "<i>" + text + "</i>"; },
    _b[rich_text_types_1.MARKS.UNDERLINE] = function (text) { return "<u>" + text + "</u>"; },
    _b[rich_text_types_1.MARKS.CODE] = function (text) { return "<code>" + text + "</code>"; },
    _b);
var defaultInline = function (type, node) {
    return "<span>type: " + type + " id: " + node.data.target.sys.id + "</span>";
};
/**
 * Serialize a Contentful Rich Text `document` to an html string.
 */
function documentToHtmlString(richTextDocument, options) {
    if (options === void 0) { options = {}; }
    if (!richTextDocument || !richTextDocument.content) {
        return '';
    }
    return nodeListToHtmlString(richTextDocument.content, {
        renderNode: __assign({}, defaultNodeRenderers, options.renderNode),
        renderMark: __assign({}, defaultMarkRenderers, options.renderMark),
    });
}
exports.documentToHtmlString = documentToHtmlString;
function nodeListToHtmlString(nodes, _a) {
    var renderNode = _a.renderNode, renderMark = _a.renderMark;
    return nodes.map(function (node) { return nodeToHtmlString(node, { renderNode: renderNode, renderMark: renderMark }); }).join('');
}
function nodeToHtmlString(node, _a) {
    var renderNode = _a.renderNode, renderMark = _a.renderMark;
    if (rich_text_types_1.helpers.isText(node)) {
        var nodeValue = escape_html_1.default(node.value);
        if (node.marks.length > 0) {
            return node.marks.reduce(function (value, mark) {
                if (!renderMark[mark.type]) {
                    return value;
                }
                return renderMark[mark.type](value);
            }, nodeValue);
        }
        return nodeValue;
    }
    else {
        var nextNode = function (nodes) { return nodeListToHtmlString(nodes, { renderMark: renderMark, renderNode: renderNode }); };
        if (!node.nodeType || !renderNode[node.nodeType]) {
            // TODO: Figure what to return when passed an unrecognized node.
            return '';
        }
        return renderNode[node.nodeType](node, nextNode);
    }
}
//# sourceMappingURL=index.js.map