"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var rich_text_types_1 = require("@contentful/rich-text-types");
var index_1 = require("../index");
var documents_1 = require("./documents");
var inline_entity_1 = __importDefault(require("./documents/inline-entity"));
describe('documentToHtmlString', function () {
    it('returns empty string when given an empty document', function () {
        var document = {
            nodeType: rich_text_types_1.BLOCKS.DOCUMENT,
            data: {},
            content: [],
        };
        expect(index_1.documentToHtmlString(document)).toEqual('');
    });
    it('renders nodes with default node renderer', function () {
        var docs = [
            {
                doc: documents_1.paragraphDoc,
                expected: '<p>hello world</p>',
            },
            {
                doc: documents_1.headingDoc(rich_text_types_1.BLOCKS.HEADING_1),
                expected: '<h1>hello world</h1>',
            },
            {
                doc: documents_1.headingDoc(rich_text_types_1.BLOCKS.HEADING_2),
                expected: '<h2>hello world</h2>',
            },
        ];
        docs.forEach(function (_a) {
            var doc = _a.doc, expected = _a.expected;
            expect(index_1.documentToHtmlString(doc)).toEqual(expected);
        });
    });
    it('renders marks with default mark renderer', function () {
        var docs = [
            {
                doc: documents_1.marksDoc(rich_text_types_1.MARKS.ITALIC),
                expected: '<p><i>hello world</i></p>',
            },
            {
                doc: documents_1.marksDoc(rich_text_types_1.MARKS.BOLD),
                expected: '<p><b>hello world</b></p>',
            },
            {
                doc: documents_1.marksDoc(rich_text_types_1.MARKS.UNDERLINE),
                expected: '<p><u>hello world</u></p>',
            },
            {
                doc: documents_1.marksDoc(rich_text_types_1.MARKS.CODE),
                expected: '<p><code>hello world</code></p>',
            },
        ];
        docs.forEach(function (_a) {
            var doc = _a.doc, expected = _a.expected;
            expect(index_1.documentToHtmlString(doc)).toEqual(expected);
        });
    });
    it('renders nodes with passed custom node renderer', function () {
        var _a;
        var options = {
            renderNode: (_a = {},
                _a[rich_text_types_1.BLOCKS.PARAGRAPH] = function (node, next) { return "<p>" + next(node.content) + "</p>"; },
                _a),
        };
        var document = documents_1.paragraphDoc;
        var expected = "<p>hello world</p>";
        expect(index_1.documentToHtmlString(document, options)).toEqual(expected);
    });
    it('renders marks with the passed custom mark rendered', function () {
        var _a;
        var options = {
            renderMark: (_a = {},
                _a[rich_text_types_1.MARKS.UNDERLINE] = function (text) { return "<u>" + text + "</u>"; },
                _a),
        };
        var document = documents_1.marksDoc(rich_text_types_1.MARKS.UNDERLINE);
        var expected = '<p><u>hello world</u></p>';
        expect(index_1.documentToHtmlString(document, options)).toEqual(expected);
    });
    it('renders escaped html', function () {
        var document = {
            nodeType: rich_text_types_1.BLOCKS.DOCUMENT,
            data: {},
            content: [
                {
                    nodeType: rich_text_types_1.BLOCKS.PARAGRAPH,
                    data: {},
                    content: [
                        {
                            nodeType: 'text',
                            value: 'foo & bar',
                            marks: [],
                            data: {},
                        },
                    ],
                },
            ],
        };
        var expected = '<p>foo &amp; bar</p>';
        expect(index_1.documentToHtmlString(document)).toEqual(expected);
    });
    it('renders escaped html with marks', function () {
        var document = {
            nodeType: rich_text_types_1.BLOCKS.DOCUMENT,
            data: {},
            content: [
                {
                    nodeType: rich_text_types_1.BLOCKS.PARAGRAPH,
                    data: {},
                    content: [
                        {
                            nodeType: 'text',
                            value: 'foo & bar',
                            marks: [{ type: rich_text_types_1.MARKS.UNDERLINE }, { type: rich_text_types_1.MARKS.BOLD }],
                            data: {},
                        },
                    ],
                },
            ],
        };
        var expected = '<p><b><u>foo &amp; bar</u></b></p>';
        expect(index_1.documentToHtmlString(document)).toEqual(expected);
    });
    it('does not render unrecognized marks', function () {
        var document = documents_1.invalidMarksDoc;
        var expected = '<p>Hello world!</p>';
        expect(index_1.documentToHtmlString(document)).toEqual(expected);
    });
    it('renders empty node if type is not recognized', function () {
        var document = documents_1.invalidTypeDoc;
        var expected = '';
        expect(index_1.documentToHtmlString(document)).toEqual(expected);
    });
    it('renders default entry link block', function () {
        var entrySys = {
            sys: {
                id: '9mpxT4zsRi6Iwukey8KeM',
                link: 'Link',
                linkType: 'Entry',
            },
        };
        var document = documents_1.embeddedEntryDoc(entrySys);
        var expected = "<div></div>";
        expect(index_1.documentToHtmlString(document)).toEqual(expected);
    });
    it('renders ordered lists', function () {
        var document = documents_1.olDoc;
        var expected = "<ol><li><p>Hello</p></li><li><p>world</p></li></ol><p></p>";
        expect(index_1.documentToHtmlString(document)).toEqual(expected);
    });
    it('renders unordered lists', function () {
        var document = documents_1.ulDoc;
        var expected = "<ul><li><p>Hello</p></li><li><p>world</p></li></ul><p></p>";
        expect(index_1.documentToHtmlString(document)).toEqual(expected);
    });
    it('renders blockquotes', function () {
        var document = documents_1.quoteDoc;
        var expected = "<p>hello</p><blockquote>world</blockquote>";
        expect(index_1.documentToHtmlString(document)).toEqual(expected);
    });
    it('renders horizontal rule', function () {
        var document = documents_1.hrDoc;
        var expected = '<p>hello world</p><hr/><p></p>';
        expect(index_1.documentToHtmlString(document)).toEqual(expected);
    });
    it('does not crash with inline elements (e.g. hyperlink)', function () {
        var document = documents_1.hyperlinkDoc;
        expect(index_1.documentToHtmlString(document)).toBeTruthy();
    });
    it('renders hyperlink', function () {
        var document = documents_1.hyperlinkDoc;
        var expected = '<p>Some text <a href="https://url.org">link</a> text.</p>';
        expect(index_1.documentToHtmlString(document)).toEqual(expected);
    });
    it("renders asset hyperlink", function () {
        var asset = {
            target: {
                sys: {
                    id: '9mpxT4zsRi6Iwukey8KeM',
                    link: 'Link',
                    type: 'Asset',
                },
            },
        };
        var document = inline_entity_1.default(asset, rich_text_types_1.INLINES.ASSET_HYPERLINK);
        var expected = "<p><span>type: " + rich_text_types_1.INLINES.ASSET_HYPERLINK + " id: " + asset.target.sys.id + "</span></p>";
        expect(index_1.documentToHtmlString(document)).toEqual(expected);
    });
    it('renders entry hyperlink', function () {
        var entry = {
            target: {
                sys: {
                    id: '9mpxT4zsRi6Iwukey8KeM',
                    link: 'Link',
                    type: 'Entry',
                },
            },
        };
        var document = inline_entity_1.default(entry, rich_text_types_1.INLINES.ENTRY_HYPERLINK);
        var expected = "<p><span>type: " + rich_text_types_1.INLINES.ENTRY_HYPERLINK + " id: " + entry.target.sys.id + "</span></p>";
        expect(index_1.documentToHtmlString(document)).toEqual(expected);
    });
    it('renders embedded entry', function () {
        var entry = {
            target: {
                sys: {
                    id: '9mpxT4zsRi6Iwukey8KeM',
                    link: 'Link',
                    type: 'Entry',
                },
            },
        };
        var document = inline_entity_1.default(entry, rich_text_types_1.INLINES.EMBEDDED_ENTRY);
        var expected = "<p><span>type: " + rich_text_types_1.INLINES.EMBEDDED_ENTRY + " id: " + entry.target.sys.id + "</span></p>";
        expect(index_1.documentToHtmlString(document)).toEqual(expected);
    });
    it('does not crash with empty documents', function () {
        expect(index_1.documentToHtmlString({})).toEqual('');
    });
    it('does not crash with undefined documents', function () {
        expect(index_1.documentToHtmlString(undefined)).toEqual('');
    });
});
//# sourceMappingURL=index.test.js.map