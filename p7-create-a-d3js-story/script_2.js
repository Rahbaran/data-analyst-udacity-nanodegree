d3.csv("description.csv", function(d) {
	return d;
}, draw);

function draw(description) {

	////////////////////////////////////////////////////////////
	//////////////////////// Set-Up ////////////////////////////
	////////////////////////////////////////////////////////////

	var margin = {left:90, top:90, right:90, bottom:90},
			width = Math.min(window.innerWidth, 1100) - margin.left - margin.right,
	    height = Math.min(window.innerWidth,1100) - margin.top - margin.bottom,
	    innerRadius = Math.min(width, height) * .39,
	    outerRadius = innerRadius * 1.1;

	var names = ["Company A1", "Company A2", "Company A3", "Company A4", "Company A5",
							 "Company B1", "Company B2", "Company B3", "Company B4", "Company B5", "Company B6", "Company B7", "Company B8", "Company B9", "Company B10", "Company B11", "Company B12", "Company B13",
						   "Company C1",
						   "Company D1", "Company D2", "Company D3",
							 "Company E1",
							 "Company F1", "Company F2", "Company F3", "Company F4",
							 "Service A1", "Service A2", "Service A3", "Service A4", "Service A5", "Service A6", "Service A7", "Service A8", "Service A9", "Service A10", "Service A11", "Service A12",	"Service A13",	"Service A14"
							],
      opacityDefault = 0.8;

			var matrix = [
				// Consal
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,0,1,1,1,1,1], // UKV
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,1,1,1,1,1,1], // URV
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,1,1,1,1,1,1], // CONSAL MaklerService
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,0,0,0,1,1,1,1,1], // Consal Versicherungsdienste
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,0,0], // Kranken-Vertrieb.de
				 // Landesdirektionen
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,0,1,1,1,1,1], // SAARLAND Versicherung
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,0,1,1,1,1,1], // Feuersozietät Berlin Brandenburg
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,0,1,1,1,1,1], // Westfälische Provinzial
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,0,1,1,1,1,1], // Provinzial Nord
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,0,0], // Hamburger Feuerkasse
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,0,1,1,1,1,1], // SV SparkassenVersicherung
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,0,1,1,1,1,1], // Provinzial Rheinland
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,0,1,1,1,1,1], // SV Sparkassen-Versicherung Sachsen
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,0,1,1,1,1,1], // Öffentliche Versicherung Braunschweig
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,0,1,1,1,1,0,0,0,0,0,0], // BGV / Badische Versicherung
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,0,0], // Öffentliche Versicherung Oldenburg
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,0,1,1,1,1,1], // ÖSA Versicherung
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,0,1,1,1,1,1], // Lippische
				//VKB
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,0,1,1,1,1,1], // Versicherungskammer Bayern
				//GKVen
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,1,1,1,0,1,1,1,1,1], // AOK Bayern
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,1,1,0,0,0,0,0,0,0,0,0], // AOK Sachsen-Anhalt
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,0,0,0,0,0,0,0,0,0,0,0], // Sozialversicherung für Landwirtschaft, Forsten und Gartenbau
				// Sparkasse IF6
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,0,0,0,1,1,1,0,0,1,1,1,1,0], // Sparkasse IF6
				 //Drittanbieter
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,0,0], // Genossenschaftsbanken
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,0,1,1,0,0,0,1,1,1,1,0], // 1822direkt
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,0,0,0,0,0,0,0], // Baden-Württembergische Bank
			  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,  1,1,1,0,1,1,0,0,0,0,0,0,0,0], // BavariaDirekt

				//Bis hier drei Hauptquadranten

				//Krankenzusatzpflege
				[1,1,1,1,0, 1,1,1,1,0,1,1,1,1,1,0,1,1, 1, 1,1,1, 1, 0,1,0,1,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // ZahnPRIVAT Premium
				[1,1,1,1,0, 1,1,1,1,0,1,1,1,1,1,0,1,1, 1, 1,1,1, 0, 0,1,0,1,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // ZahnPRIVAT Optimal
				[1,1,1,1,0, 1,1,1,1,0,1,1,1,1,1,0,1,1, 1, 1,1,1, 0, 0,1,0,1,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // ZahnPRIVAT Kompakt
				[1,1,1,1,0, 1,1,1,1,0,1,1,1,1,0,0,1,1, 1, 1,1,0, 0, 0,0,0,0,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // ZahnVITAL
				[1,1,1,1,0, 1,1,1,1,0,1,1,1,1,1,0,1,1, 1, 1,1,0, 1, 0,1,0,1,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // NaturPRIVAT
				[1,1,1,1,0, 1,1,1,1,0,1,1,1,1,1,0,1,1, 1, 1,0,0, 1, 0,1,0,1,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // VorsorgePRIVAT
				[1,1,1,0,0, 1,1,1,1,0,1,1,1,1,1,0,1,1, 1, 1,0,0, 1, 0,0,0,0,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // KlinikPRIVAT 2
				[1,1,1,0,0, 1,1,1,1,0,1,1,1,1,1,0,1,1, 1, 1,0,0, 0, 0,0,0,0,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // KlinikPRIVAT 1
				[0,1,1,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0, 0, 0,0,0, 0, 0,0,0,0,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // ExpertPLUS
				[1,1,1,1,0, 1,1,1,1,0,1,1,1,1,0,0,1,1, 1, 1,0,0, 1, 0,1,0,0,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // S-KG 600
				[1,1,1,1,0, 1,1,1,1,0,1,1,1,1,0,0,1,1, 1, 1,0,0, 1, 0,1,0,0,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // S-KG 450
				[1,1,1,1,0, 1,1,1,1,0,1,1,1,1,0,0,1,1, 1, 1,0,0, 1, 0,1,0,0,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // S-KG 300
				[1,1,1,1,0, 1,1,1,1,0,1,1,1,1,0,0,1,1, 1, 1,0,0, 1, 0,1,0,0,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // S-KG 150
				[1,1,1,1,0, 1,1,1,1,0,1,1,1,1,0,0,1,1, 1, 1,0,0, 0, 0,0,0,0,   0,0,0,0,0,0,0,0,0,0,0,0,0,0], // Krankenhaustagegeld

			];

	//define grouping with colors
	var groups = [
		{sIndex:  0, eIndex:  4, title: 'Companies As', color: '#004F9F'},
		{sIndex:  5, eIndex: 17, title: 'Companies Bs', color: '#df7c00'},
		{sIndex: 18, eIndex: 18, title: 'Company C', color: '#0D57A6'},
		{sIndex: 19, eIndex: 21, title: 'Companies Ds', color: '#008A34'},
		{sIndex: 22, eIndex: 22, title: 'Company E', color: '#FF0000'},
		{sIndex: 23, eIndex: 26, title: 'Companies F', color: 'purple'},
		{sIndex: 27, eIndex: 41, title: 'Services A', color: 'rgb(233,233,233,0.2)'}
	];

	var tip = d3.tip()
	      .attr('class', 'd3-tip')
	      .offset([-10, 0])
	      .html(function(d, i) {
	        return "<emphasis>Unternehmensauftritt der</emphasis> " + names[d.index] + description[d.index].description;
	      })

	////////////////////////////////////////////////////////////
	/////////// Create scale and layout functions //////////////
	////////////////////////////////////////////////////////////

	var colors = d3.scaleOrdinal()
	    .domain(d3.range(names.length));
			//.range(colors);

	var chord = d3.chord()
	    .padAngle(.012)
	    .sortChords(d3.descending);

	var arc = d3.arc()
	    .innerRadius(innerRadius*1.01)
	    .outerRadius(outerRadius);

	var path = d3.ribbon()
			.radius(innerRadius);

	////////////////////////////////////////////////////////////
	////////////////////// Create SVG + initialize TT///////////
	////////////////////////////////////////////////////////////

	var svg = d3.select("#chart").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
			.append("g")
	    .attr("transform", "translate(" + (width/2 + margin.left) + "," + (height/2 + margin.top) + ")")
			.datum(chord(matrix));

	// initialize tip
	svg.call(tip);

	////////////////////////////////////////////////////////////
	/////////////// Create the gradient fills //////////////////
	////////////////////////////////////////////////////////////

	//Function to create the unique id for each chord gradient
	function getGradID(d){ return "linkGrad-" + d.source.index + "-" + d.target.index; }

	//Create the gradients definitions for each chord
	var grads = svg.append("defs").selectAll("linearGradient")
		.data(function(chords) { return chords; })
	   .enter().append("linearGradient")
	    //Create the unique ID for this specific source-target pairing
		.attr("id", getGradID)
		.attr("gradientUnits", "userSpaceOnUse")
		//Find the location where the source chord starts
		.attr("x1", function(d,i) { return innerRadius * Math.cos((d.source.endAngle-d.source.startAngle)/2 + d.source.startAngle - Math.PI/2); })
		.attr("y1", function(d,i) { return innerRadius * Math.sin((d.source.endAngle-d.source.startAngle)/2 + d.source.startAngle - Math.PI/2); })
		//Find the location where the target chord starts
		.attr("x2", function(d,i) { return innerRadius * Math.cos((d.target.endAngle-d.target.startAngle)/2 + d.target.startAngle - Math.PI/2); })
		.attr("y2", function(d,i) { return innerRadius * Math.sin((d.target.endAngle-d.target.startAngle)/2 + d.target.startAngle - Math.PI/2); })

	//Set the starting color (at 0%)
	grads.append("stop")
		.attr("offset", "0%")
		.attr("stop-color", function(d){ return colors(d.source.index); });

	//Set the ending color (at 100%)
	grads.append("stop")
		.attr("offset", "100%")
		.attr("stop-color", function(d){ return colors(d.target.index); });

	////////////////////////////////////////////////////////////
	////////////////// Draw outer Arcs /////////////////////////
	////////////////////////////////////////////////////////////

	var outerArcs = svg.selectAll("g.group")
		.data(function(d) { return d.groups; })
		.enter().append("g")
		.attr("class", "group")
		.on("mouseover", function(d,i){
			fade(.1)(d,i);
			tip.show(d);
		})
		.on("mouseout", function(d,i){
			// ??! fade(opacityDefault, tip.hide);
			fade(.8)(d,i);
			tip.hide(d);
		});
		// former ways of calling fade() on mouseover
		//.on("mouseover", fade(.1))
		//.on("mouseout", fade(opacityDefault, tip.hide));

	outerArcs.append("path")
		.style("fill", function(d) {
			var thisGroup = groups.filter(function(e) {
					return (d.index >= e.sIndex && d.index <= e.eIndex);
			});
			return thisGroup[0] ? thisGroup[0].color : "gray";
		})
		.attr("d", arc);

	////////////////////////////////////////////////////////////
	////////////////////// Append names ////////////////////////
	////////////////////////////////////////////////////////////

	//Append the label names on the outside
	outerArcs.append("text")
	  .each(function(d) { d.angle = (d.startAngle + d.endAngle) / 2; })
	  .attr("dy", ".35em")
	  .attr("class", "titles")
	  .attr("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
	  .attr("transform", function(d) {
			return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")"
			+ "translate(" + (outerRadius + 10) + ")"
			+ (d.angle > Math.PI ? "rotate(180)" : "");
	  })
	  .text(function(d,i) { return names[i]; });

	////////////////////////////////////////////////////////////
	////////////////// Draw inner chords ///////////////////////
	////////////////////////////////////////////////////////////

	svg.selectAll("path.chord")
		.data(function(chords) { return chords; })
		.enter().append("path")
		.attr("class", "chord")
		//change the fill to reference the unique gradient ID of the source-target combination
		//.style("fill", function(d){ return "url(#" + getGradID(d) + ")"; })
		// alternative no gradients:
		.style("fill", function(d) {
			var thisGroup = groups.filter(function(e) {
					return (d.source.index >= e.sIndex && d.source.index <= e.eIndex);
			});
			return thisGroup[0] ? thisGroup[0].color : "gray";
		})
		.style("opacity", opacityDefault)
		.attr("d", path)
		.on("mouseover", mouseoverChord)
		.on("mouseout", mouseoutChord);

	// names for legend, not working properly
	// for(var i=0;i<groups.length;i++) {
	// 	var __g = groups[i];
	// 	// Add a text label.
	// 	var text = svg.append("text")
	// 		.attr("x", 200 + i*120)
	// 		.attr("dx", 20 + i*110)
	// 		.attr("dy", 20 + i*200);
	//
	// 	text.append("textPath")
	// 		// .attr("stroke","#fff")
	// 		.attr('fill', 'blue')
	// 		.attr("xlink:href","#groupId" + i)
	// 		.text(__g.title);
	// }
	////////////////////////////////////////////////////////////
	////////////////// Extra Functions /////////////////////////
	////////////////////////////////////////////////////////////

	//Returns an event handler for fading a given chord group.
	function fade(opacity) {
			console.log(opacity);
	  return function(d,i) {
		console.log(d);
		console.log(i);
	    svg.selectAll("path.chord")
	        .filter(function(d) { return d.source.index != i && d.target.index != i; })
			.transition()
	        .style("opacity", opacity);
	  };
	}//fade

	//Highlight hovered over chord
	function mouseoverChord(d,i) {
		//Decrease opacity to all
		svg.selectAll("path.chord")
			.transition()
			.style("opacity", 0.1);
		//Show hovered over chord with full opacity
		d3.select(this)
			.transition()
			.style("opacity", 1);
		//correct log
		//console.log("i: " + d.source.index);
		//Define and show the tooltip over the mouse location
		$(this).popover({
			//placement: 'auto top',
			title: function() {return names[d.source.index];},
			placement: 'auto',
			container: 'body',
			animation: false,
			followMouse: true,
			trigger: 'click',
			html : true,
			content: function() {
			return "<p style='font-size: 11px; text-align: center;'><span style='font-weight:900'>" + names[d.target.index] + "</span> is embedded in " + "<span style='font-weight:900'>" + names[d.source.index] + "</span><span style='font-weight:900'></span></p>"; }
		});
		$(this).popover('show');
	}
	//Bring all chords back to default opacity
	function mouseoutChord(d) {
		//Hide the tooltip
		$('.popover').each(function() {
			$(this).remove();
		})
		//Set opacity back to default for all
		svg.selectAll("path.chord")
			.transition()
			.style("opacity", opacityDefault);
		}      //function mouseoutChord
}
